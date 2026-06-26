# -*- coding: utf-8 -*-
"""
D'TALE Student Portal
======================
Admin + Student login, student self-registration with auto-generated
credentials delivered as a PDF, 42 chapters x 50 assignments each, 10
capstone projects, and progress-gated unlocking (finish all 50 assignments
in a chapter to unlock the next one; finish all 42 chapters to unlock the
projects; finish a project to unlock the next one).

Run with:
    pip install flask reportlab
    python app.py
Then open http://127.0.0.1:5000
"""
import os
from flask import Flask, request, redirect, url_for, session, send_file, abort, Response
from werkzeug.security import generate_password_hash, check_password_hash

import db
import data
import helpers
import assignments as A
from credentials_pdf import build_credentials_pdf
from templates import (
    render_landing, render_admin_login, render_student_login, render_register,
    render_register_success, render_dashboard, render_chapter, render_project,
    render_admin_dashboard, render_admin_student_detail,
)

app = Flask(__name__)
app.secret_key = os.environ.get("DTALE_SECRET_KEY", "dev-secret-change-me-in-production")

ADMIN_USERNAME = os.environ.get("DTALE_ADMIN_USERNAME", "Arabinda")
ADMIN_PASSWORD = os.environ.get("DTALE_ADMIN_PASSWORD")

if not ADMIN_PASSWORD:
    raise RuntimeError(
        "DTALE_ADMIN_PASSWORD environment variable is not set. "
        "Set it in your Render service's Environment tab."
    )


# ---------------------------------------------------------------- bootstrap
def bootstrap():
    db.init_db()
    db.seed_admin(ADMIN_USERNAME, generate_password_hash(ADMIN_PASSWORD))


bootstrap()


# ---------------------------------------------------------------- helpers
def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return db.get_user_by_id(uid)


def require_login(role=None):
    user = current_user()
    if user is None:
        return None
    if role and user["role"] != role:
        return None
    return user


def chapter_by_id(cid):
    for c in data.CHAPTERS:
        if c["id"] == cid:
            return c
    return None


def project_by_id(pid):
    for p in data.PROJECTS:
        if p["id"] == pid:
            return p
    return None


def compute_unlock_state(user_id):
    """
    Returns:
      chapter_status: {chapter_id: 'done' | 'unlocked' | 'locked'}
      project_status: {project_id: 'done' | 'unlocked' | 'locked'}
    Chapter 1 always unlocked. Chapter N+1 unlocks only once chapter N is done.
    Project 1 unlocks only once ALL 42 chapters are done. Project N+1 unlocks
    once project N is done.
    """
    progress = db.get_all_chapter_progress(user_id)
    chapter_status = {}
    prev_done = True
    for c in data.CHAPTERS:
        cid = c["id"]
        done = progress.get(cid, {}).get("completed", False)
        if done:
            chapter_status[cid] = "done"
        elif prev_done:
            chapter_status[cid] = "unlocked"
        else:
            chapter_status[cid] = "locked"
        prev_done = done

    all_chapters_done = all(chapter_status[c["id"]] == "done" for c in data.CHAPTERS)

    proj_progress = db.get_all_project_progress(user_id)
    project_status = {}
    prev_done = all_chapters_done
    for p in data.PROJECTS:
        pid = p["id"]
        done = proj_progress.get(pid, False)
        if done:
            project_status[pid] = "done"
        elif prev_done:
            project_status[pid] = "unlocked"
        else:
            project_status[pid] = "locked"
        prev_done = done

    return chapter_status, project_status


# ---------------------------------------------------------------- landing / auth
@app.route("/")
def landing():
    return render_landing()


@app.route("/login/admin", methods=["GET", "POST"])
def login_admin():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = db.get_user_by_username(username)
        if user and user["role"] == "admin" and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["role"] = "admin"
            return redirect(url_for("admin_dashboard"))
        error = "Incorrect ID or password."
    return render_admin_login(error)


@app.route("/login/student", methods=["GET", "POST"])
def login_student():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = db.get_user_by_username(username)
        if user and user["role"] == "student" and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["role"] = "student"
            return redirect(url_for("dashboard"))
        error = "Incorrect ID or password. Check the PDF you received at registration."
    return render_student_login(error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        if not name or not email or not phone:
            error = "Please fill in your name, email, and phone number."
        else:
            username = helpers.generate_username(name)
            password = helpers.generate_password(name)
            user_id = db.create_student(username, generate_password_hash(password), name, email, phone)
            session["just_registered_id"] = user_id
            return redirect(url_for("register_success", uid=user_id))
    return render_register(error)


@app.route("/register/success/<int:uid>")
def register_success(uid):
    # Only viewable right after registration in this same browser session
    if session.get("just_registered_id") != uid:
        return redirect(url_for("login_student"))
    user = db.get_user_by_id(uid)
    if user is None:
        abort(404)
    return render_register_success(user)


@app.route("/register/pdf/<int:uid>")
def register_pdf(uid):
    if session.get("just_registered_id") != uid:
        abort(403)
    user = db.get_user_by_id(uid)
    if user is None:
        abort(404)
    # We never stored the plaintext password -- but we can deterministically
    # regenerate it from the stored name, since the rule is fixed (FirstName@123).
    password = helpers.generate_password(user["name"])
    buf = build_credentials_pdf(user["name"], user["username"], password, user["email"], user["phone"])
    return send_file(
        buf, mimetype="application/pdf", as_attachment=True,
        download_name=f"dtale-login-{user['username']}.pdf",
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


# ---------------------------------------------------------------- student area
@app.route("/dashboard")
def dashboard():
    user = require_login("student")
    if not user:
        return redirect(url_for("login_student"))
    chapter_status, project_status = compute_unlock_state(user["id"])
    return render_dashboard(user, data.CHAPTERS, data.PROJECTS, chapter_status, project_status)


@app.route("/chapter/<int:cid>")
def chapter_view(cid):
    user = require_login("student")
    if not user:
        return redirect(url_for("login_student"))
    chapter = chapter_by_id(cid)
    if chapter is None:
        abort(404)
    chapter_status, _ = compute_unlock_state(user["id"])
    if chapter_status.get(cid) == "locked":
        return render_chapter(user, chapter, [], set(), locked=True)
    prog = db.get_chapter_progress(user["id"], cid)
    assignment_list = A.generate_assignments(chapter)
    return render_chapter(user, chapter, assignment_list, set(prog["done_indices"]), locked=False)


@app.route("/chapter/<int:cid>/toggle/<int:idx>", methods=["POST"])
def chapter_toggle(cid, idx):
    user = require_login("student")
    if not user:
        abort(403)
    chapter_status, _ = compute_unlock_state(user["id"])
    if chapter_status.get(cid) == "locked":
        abort(403)
    if idx < 0 or idx > 49:
        abort(400)
    db.toggle_assignment(user["id"], cid, idx, total=50)
    return redirect(url_for("chapter_view", cid=cid))


@app.route("/project/<int:pid>")
def project_view(pid):
    user = require_login("student")
    if not user:
        return redirect(url_for("login_student"))
    proj = project_by_id(pid)
    if proj is None:
        abort(404)
    _, project_status = compute_unlock_state(user["id"])
    locked = project_status.get(pid) == "locked"
    done = project_status.get(pid) == "done"
    return render_project(user, proj, locked=locked, done=done)


@app.route("/project/<int:pid>/complete", methods=["POST"])
def project_complete(pid):
    user = require_login("student")
    if not user:
        abort(403)
    _, project_status = compute_unlock_state(user["id"])
    if project_status.get(pid) == "locked":
        abort(403)
    db.toggle_project(user["id"], pid)
    return redirect(url_for("project_view", pid=pid))


# ---------------------------------------------------------------- admin area
@app.route("/admin")
def admin_dashboard():
    user = require_login("admin")
    if not user:
        return redirect(url_for("login_admin"))
    students = db.all_students()
    rows = []
    for s in students:
        chapter_status, project_status = compute_unlock_state(s["id"])
        done_chapters = sum(1 for v in chapter_status.values() if v == "done")
        done_projects = sum(1 for v in project_status.values() if v == "done")
        rows.append({"user": s, "done_chapters": done_chapters, "done_projects": done_projects})
    return render_admin_dashboard(user, rows)


@app.route("/admin/student/<int:sid>")
def admin_student_detail(sid):
    user = require_login("admin")
    if not user:
        return redirect(url_for("login_admin"))
    student = db.get_user_by_id(sid)
    if student is None or student["role"] != "student":
        abort(404)
    chapter_status, project_status = compute_unlock_state(sid)
    return render_admin_student_detail(user, student, data.CHAPTERS, data.PROJECTS, chapter_status, project_status)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
