# -*- coding: utf-8 -*-
"""Tiny SQLite layer for the D'TALE Student Portal. No ORM, just sqlite3."""
import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dtale_portal.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,              -- 'admin' or 'student'
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT,
            email TEXT,
            phone TEXT,
            created_at TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS chapter_progress (
            user_id INTEGER NOT NULL,
            chapter_id INTEGER NOT NULL,
            done_indices TEXT NOT NULL DEFAULT '[]',   -- JSON list of completed assignment indices (0-49)
            completed INTEGER NOT NULL DEFAULT 0,
            completed_at TEXT,
            PRIMARY KEY (user_id, chapter_id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS project_progress (
            user_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            completed_at TEXT,
            PRIMARY KEY (user_id, project_id)
        )
    """)
    conn.commit()
    conn.close()


def seed_admin(username, password_hash):
    conn = get_conn()
    c = conn.cursor()
    existing = c.execute("SELECT id FROM users WHERE role='admin' AND username=?", (username,)).fetchone()
    if not existing:
        c.execute(
            "INSERT INTO users (role, username, password_hash, name, email, phone, created_at) VALUES (?,?,?,?,?,?,?)",
            ("admin", username, password_hash, "Administrator", "", "", datetime.utcnow().isoformat()),
        )
        conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def username_exists(username):
    return get_user_by_username(username) is not None


def create_student(username, password_hash, name, email, phone):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (role, username, password_hash, name, email, phone, created_at) VALUES (?,?,?,?,?,?,?)",
        ("student", username, password_hash, name, email, phone, datetime.utcnow().isoformat()),
    )
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return user_id


def all_students():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM users WHERE role='student' ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows


# ---------- chapter progress ----------

def get_chapter_progress(user_id, chapter_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM chapter_progress WHERE user_id=? AND chapter_id=?", (user_id, chapter_id)
    ).fetchone()
    conn.close()
    if row is None:
        return {"done_indices": [], "completed": False}
    return {"done_indices": json.loads(row["done_indices"]), "completed": bool(row["completed"])}


def get_all_chapter_progress(user_id):
    """-> {chapter_id: {'done_indices': [...], 'completed': bool}}"""
    conn = get_conn()
    rows = conn.execute("SELECT * FROM chapter_progress WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    out = {}
    for row in rows:
        out[row["chapter_id"]] = {"done_indices": json.loads(row["done_indices"]), "completed": bool(row["completed"])}
    return out


def toggle_assignment(user_id, chapter_id, index, total=50):
    """Flip one assignment's done state. Returns (done_indices, completed)."""
    conn = get_conn()
    c = conn.cursor()
    row = c.execute(
        "SELECT * FROM chapter_progress WHERE user_id=? AND chapter_id=?", (user_id, chapter_id)
    ).fetchone()
    if row is None:
        done = []
    else:
        done = json.loads(row["done_indices"])

    if index in done:
        done.remove(index)
    else:
        done.append(index)

    completed = 1 if len(done) >= total else 0
    completed_at = datetime.utcnow().isoformat() if completed else None

    if row is None:
        c.execute(
            "INSERT INTO chapter_progress (user_id, chapter_id, done_indices, completed, completed_at) VALUES (?,?,?,?,?)",
            (user_id, chapter_id, json.dumps(done), completed, completed_at),
        )
    else:
        c.execute(
            "UPDATE chapter_progress SET done_indices=?, completed=?, completed_at=? WHERE user_id=? AND chapter_id=?",
            (json.dumps(done), completed, completed_at, user_id, chapter_id),
        )
    conn.commit()
    conn.close()
    return done, bool(completed)


# ---------- project progress ----------

def get_all_project_progress(user_id):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM project_progress WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return {row["project_id"]: bool(row["completed"]) for row in rows}


def toggle_project(user_id, project_id):
    conn = get_conn()
    c = conn.cursor()
    row = c.execute(
        "SELECT * FROM project_progress WHERE user_id=? AND project_id=?", (user_id, project_id)
    ).fetchone()
    if row is None:
        c.execute(
            "INSERT INTO project_progress (user_id, project_id, completed, completed_at) VALUES (?,?,?,?)",
            (user_id, project_id, 1, datetime.utcnow().isoformat()),
        )
        new_state = True
    else:
        new_state = not bool(row["completed"])
        c.execute(
            "UPDATE project_progress SET completed=?, completed_at=? WHERE user_id=? AND project_id=?",
            (1 if new_state else 0, datetime.utcnow().isoformat() if new_state else None, user_id, project_id),
        )
    conn.commit()
    conn.close()
    return new_state
