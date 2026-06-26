# -*- coding: utf-8 -*-
"""Postgres data layer for the D'TALE Student Portal.

Replaces the old SQLite version. SQLite stored its file on local disk,
which Render wipes every time the free-tier service spins down/restarts/
redeploys -- so registered students kept disappearing. This version talks
to a Render PostgreSQL database instead, which persists independently of
the web service.

Requires the DATABASE_URL environment variable to be set (Render provides
this automatically once you create a PostgreSQL instance and link it, or
you paste the Internal Database URL into your web service's Environment
tab).

All function names and return shapes are kept identical to the old
db.py, so app.py does not need any changes.
"""
import os
import json
from datetime import datetime

import psycopg2
import psycopg2.extras
from psycopg2.pool import SimpleConnectionPool

DATABASE_URL = os.environ.get("DATABASE_URL", "")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Create a PostgreSQL instance on Render "
        "and add its Internal Database URL as the DATABASE_URL environment "
        "variable on this web service."
    )

# Render sometimes hands out "postgres://" URLs; psycopg2 wants "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Small connection pool so we're not opening a brand new TCP connection to
# Postgres on every single request.
_pool = SimpleConnectionPool(1, 10, dsn=DATABASE_URL)


def get_conn():
    return _pool.getconn()


def put_conn(conn):
    _pool.putconn(conn)


def init_db():
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
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
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                completed_at TEXT,
                PRIMARY KEY (user_id, chapter_id)
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS project_progress (
                user_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                completed_at TEXT,
                PRIMARY KEY (user_id, project_id)
            )
        """)
        conn.commit()
    finally:
        put_conn(conn)


def seed_admin(username, password_hash):
    """Ensure exactly one admin row exists matching the given username, and
    keep its password hash in sync with whatever DTALE_ADMIN_PASSWORD is set
    to. This runs on every restart, so rotating the password just means
    changing the env var and redeploying -- no manual SQL needed."""
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE role='admin' AND username=%s", (username,))
        existing = c.fetchone()
        if not existing:
            c.execute(
                "INSERT INTO users (role, username, password_hash, name, email, phone, created_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                ("admin", username, password_hash, "Administrator", "", "", datetime.utcnow().isoformat()),
            )
        else:
            c.execute(
                "UPDATE users SET password_hash=%s WHERE role='admin' AND username=%s",
                (password_hash, username),
            )
        conn.commit()
    finally:
        put_conn(conn)


def get_user_by_username(username):
    conn = get_conn()
    try:
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute("SELECT * FROM users WHERE username = %s", (username,))
        return c.fetchone()
    finally:
        put_conn(conn)


def get_user_by_id(user_id):
    conn = get_conn()
    try:
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return c.fetchone()
    finally:
        put_conn(conn)


def username_exists(username):
    return get_user_by_username(username) is not None


def create_student(username, password_hash, name, email, phone):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (role, username, password_hash, name, email, phone, created_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id",
            ("student", username, password_hash, name, email, phone, datetime.utcnow().isoformat()),
        )
        user_id = c.fetchone()[0]
        conn.commit()
        return user_id
    finally:
        put_conn(conn)


def all_students():
    conn = get_conn()
    try:
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute("SELECT * FROM users WHERE role='student' ORDER BY created_at DESC")
        return c.fetchall()
    finally:
        put_conn(conn)


# ---------- chapter progress ----------

def get_chapter_progress(user_id, chapter_id):
    conn = get_conn()
    try:
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute(
            "SELECT * FROM chapter_progress WHERE user_id=%s AND chapter_id=%s",
            (user_id, chapter_id),
        )
        row = c.fetchone()
        if row is None:
            return {"done_indices": [], "completed": False}
        return {"done_indices": json.loads(row["done_indices"]), "completed": bool(row["completed"])}
    finally:
        put_conn(conn)


def get_all_chapter_progress(user_id):
    """-> {chapter_id: {'done_indices': [...], 'completed': bool}}"""
    conn = get_conn()
    try:
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute("SELECT * FROM chapter_progress WHERE user_id=%s", (user_id,))
        rows = c.fetchall()
        out = {}
        for row in rows:
            out[row["chapter_id"]] = {
                "done_indices": json.loads(row["done_indices"]),
                "completed": bool(row["completed"]),
            }
        return out
    finally:
        put_conn(conn)


def toggle_assignment(user_id, chapter_id, index, total=50):
    """Flip one assignment's done state. Returns (done_indices, completed)."""
    conn = get_conn()
    try:
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute(
            "SELECT * FROM chapter_progress WHERE user_id=%s AND chapter_id=%s",
            (user_id, chapter_id),
        )
        row = c.fetchone()
        done = json.loads(row["done_indices"]) if row is not None else []

        if index in done:
            done.remove(index)
        else:
            done.append(index)

        completed = len(done) >= total
        completed_at = datetime.utcnow().isoformat() if completed else None

        c.execute(
            """
            INSERT INTO chapter_progress (user_id, chapter_id, done_indices, completed, completed_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id, chapter_id) DO UPDATE
                SET done_indices = EXCLUDED.done_indices,
                    completed = EXCLUDED.completed,
                    completed_at = EXCLUDED.completed_at
            """,
            (user_id, chapter_id, json.dumps(done), completed, completed_at),
        )
        conn.commit()
        return done, completed
    finally:
        put_conn(conn)


# ---------- project progress ----------

def get_all_project_progress(user_id):
    conn = get_conn()
    try:
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute("SELECT * FROM project_progress WHERE user_id=%s", (user_id,))
        rows = c.fetchall()
        return {row["project_id"]: bool(row["completed"]) for row in rows}
    finally:
        put_conn(conn)


def toggle_project(user_id, project_id):
    conn = get_conn()
    try:
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute(
            "SELECT * FROM project_progress WHERE user_id=%s AND project_id=%s",
            (user_id, project_id),
        )
        row = c.fetchone()

        if row is None:
            new_state = True
            c.execute(
                "INSERT INTO project_progress (user_id, project_id, completed, completed_at) "
                "VALUES (%s,%s,%s,%s)",
                (user_id, project_id, True, datetime.utcnow().isoformat()),
            )
        else:
            new_state = not bool(row["completed"])
            c.execute(
                "UPDATE project_progress SET completed=%s, completed_at=%s "
                "WHERE user_id=%s AND project_id=%s",
                (
                    new_state,
                    datetime.utcnow().isoformat() if new_state else None,
                    user_id,
                    project_id,
                ),
            )
        conn.commit()
        return new_state
    finally:
        put_conn(conn)
