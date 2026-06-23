# -*- coding: utf-8 -*-
"""All HTML for the D'TALE Student Portal, as plain Python string templates."""

BASE_CSS = """
:root{
  --bg:#070C1E; --card:#FFFFFF; --card-2:#F4F6FB; --line:#E7E9F2;
  --ink:#10162C; --ink-dim:#5B6479; --ink-faint:#8891A3;
  --gold:#FFC524; --gold-deep:#E6A300;
  --p1:#6C4FD1; --p2:#1565C0; --p3:#0F9C81; --p4:#E0622C; --p5:#3E5C9A;
  --display:'Poppins',sans-serif; --body:'Inter',sans-serif; --mono:'JetBrains Mono',monospace;
}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:#fff;font-family:var(--body);min-height:100vh;}
h1,h2,h3,h4{font-family:var(--display);margin:0;}
a{color:inherit;text-decoration:none;}
.wrap{max-width:1100px;margin:0 auto;padding:0 24px;}
.topbar{display:flex;align-items:center;justify-content:space-between;padding:18px 0;border-bottom:1px solid rgba(255,255,255,0.1);}
.brand{display:flex;align-items:center;gap:10px;font-family:var(--display);font-weight:800;font-size:17px;}
.brand .dot{width:9px;height:9px;border-radius:50%;background:var(--gold);}
.topnav a{font-family:var(--mono);font-size:12px;color:rgba(255,255,255,0.7);padding:8px 14px;border:1px solid rgba(255,255,255,0.15);border-radius:20px;margin-left:8px;}
.topnav a:hover{color:#fff;border-color:rgba(255,255,255,0.4);}
.center-screen{min-height:80vh;display:flex;align-items:center;justify-content:center;padding:40px 16px;}
.auth-card{background:#fff;color:var(--ink);border-radius:18px;padding:40px 36px;max-width:420px;width:100%;box-shadow:0 30px 80px rgba(0,0,0,0.4);}
.auth-card h2{font-size:24px;margin-bottom:6px;}
.auth-card .sub{color:var(--ink-dim);font-size:13.5px;margin-bottom:26px;}
.field{margin-bottom:16px;}
.field label{display:block;font-family:var(--mono);font-size:11px;letter-spacing:0.05em;color:var(--ink-faint);text-transform:uppercase;margin-bottom:6px;}
.field input{width:100%;padding:11px 14px;border:1.5px solid var(--line);border-radius:9px;font-size:14.5px;font-family:var(--body);background:var(--card-2);color:var(--ink);}
.field input:focus{outline:none;border-color:var(--gold-deep);}
.btn{display:inline-block;width:100%;text-align:center;padding:13px;border-radius:9px;border:none;font-family:var(--display);font-weight:700;font-size:14.5px;cursor:pointer;}
.btn-gold{background:var(--gold);color:#10162C;}
.btn-gold:hover{background:var(--gold-deep);}
.btn-outline{background:transparent;border:1.5px solid var(--line);color:var(--ink);}
.error-box{background:#FDEAEA;color:#B42318;border:1px solid #F6C6C2;border-radius:9px;padding:10px 14px;font-size:13px;margin-bottom:16px;}
.success-box{background:#E6F7EF;color:#0F7A4F;border:1px solid #B9E8D2;border-radius:9px;padding:10px 14px;font-size:13px;margin-bottom:16px;}
.choice-grid{display:flex;gap:18px;max-width:680px;width:100%;flex-wrap:wrap;}
.choice-grid .choice-card{flex:1;min-width:260px;}
.choice-card{background:#fff;color:var(--ink);border-radius:18px;padding:34px 26px;text-align:center;box-shadow:0 30px 80px rgba(0,0,0,0.35);transition:transform .15s ease;}
.choice-card:hover{transform:translateY(-4px);}
.choice-card .ico{font-size:36px;margin-bottom:14px;}
.choice-card h3{font-size:18px;margin-bottom:8px;}
.choice-card p{font-size:13px;color:var(--ink-dim);margin:0 0 20px;}
.muted-link{display:block;text-align:center;margin-top:18px;font-size:13px;color:var(--ink-faint);}
.muted-link a{color:var(--gold-deep);font-weight:600;}
.dim-link-light{display:block;text-align:center;margin-top:22px;font-size:13px;color:rgba(255,255,255,0.65);}
.dim-link-light a{color:var(--gold);font-weight:600;}

.page{padding:34px 0 70px;}
.page h1{color:#fff;font-size:28px;margin-bottom:6px;}
.page .sub{color:rgba(255,255,255,0.6);font-size:14px;margin-bottom:28px;}

.progress-summary{display:flex;gap:20px;margin-bottom:30px;flex-wrap:wrap;}
.stat{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:14px 20px;min-width:120px;}
.stat b{display:block;font-family:var(--display);font-size:24px;color:var(--gold);}
.stat span{font-size:11px;color:rgba(255,255,255,0.6);font-family:var(--mono);text-transform:uppercase;letter-spacing:0.05em;}

.chapter-grid{display:flex;flex-wrap:wrap;gap:14px;margin-bottom:40px;}
.chapter-grid > *{flex:1;min-width:260px;}
.ch-card{background:#fff;border-radius:14px;padding:18px 20px;color:var(--ink);position:relative;overflow:hidden;}
.ch-card.locked{background:rgba(255,255,255,0.04);color:rgba(255,255,255,0.4);}
.ch-card .ch-num{font-family:var(--mono);font-size:11px;color:var(--ink-faint);}
.ch-card.locked .ch-num{color:rgba(255,255,255,0.35);}
.ch-card h4{font-size:14.5px;margin:4px 0 10px;line-height:1.3;}
.ch-card .ch-bar-track{height:6px;background:var(--card-2);border-radius:4px;overflow:hidden;margin-bottom:8px;}
.ch-card.locked .ch-bar-track{background:rgba(255,255,255,0.08);}
.ch-card .ch-bar-fill{height:100%;background:var(--gold-deep);}
.ch-card .ch-foot{display:flex;justify-content:space-between;align-items:center;font-size:11.5px;font-family:var(--mono);color:var(--ink-faint);}
.ch-card.locked .ch-foot{color:rgba(255,255,255,0.35);}
.badge-done{background:#0F9C81;color:#fff;font-size:10px;font-family:var(--mono);padding:2px 8px;border-radius:10px;}
.badge-lock{font-size:15px;}
.ch-card-link{display:block;}

.proj-grid{display:flex;flex-wrap:wrap;gap:14px;}
.proj-grid > *{flex:1;min-width:280px;}
.proj-card{background:#fff;border-radius:14px;padding:18px 20px;color:var(--ink);}
.proj-card.locked{background:rgba(255,255,255,0.04);color:rgba(255,255,255,0.4);}
.proj-card h4{font-size:15px;margin:6px 0 4px;}
.proj-card .ptag{font-family:var(--mono);font-size:10px;color:var(--gold-deep);text-transform:uppercase;letter-spacing:0.05em;}
.proj-card.locked .ptag{color:rgba(255,255,255,0.4);}
.proj-card p{font-size:12.5px;color:var(--ink-dim);margin:6px 0 0;}
.proj-card.locked p{color:rgba(255,255,255,0.35);}

.section-label{font-family:var(--mono);font-size:12px;letter-spacing:0.1em;color:var(--gold);text-transform:uppercase;margin:36px 0 14px;}

.chapter-detail{background:#fff;color:var(--ink);border-radius:16px;padding:30px 32px;}
.chapter-detail .ch-head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;flex-wrap:wrap;gap:10px;}
.chapter-detail h2{font-size:24px;}
.chapter-detail .ch-part{font-family:var(--mono);font-size:11px;color:var(--ink-faint);text-transform:uppercase;letter-spacing:0.05em;}
.progress-pill{font-family:var(--mono);font-size:12px;background:var(--card-2);padding:6px 14px;border-radius:20px;color:var(--ink);white-space:nowrap;}
.assignment-list{margin-top:24px;border-top:1px solid var(--line);}
.assignment-row{display:flex;align-items:flex-start;gap:12px;padding:13px 4px;border-bottom:1px solid var(--line);}
.assignment-row.done{background:#F8FBF9;}
.assignment-row form{flex-shrink:0;margin-top:1px;}
.assignment-row .chk-btn{width:22px;height:22px;border-radius:6px;border:2px solid var(--line);background:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:13px;color:#fff;padding:0;}
.assignment-row.done .chk-btn{background:#0F9C81;border-color:#0F9C81;}
.assignment-row .a-num{font-family:var(--mono);font-size:11px;color:var(--ink-faint);width:26px;flex-shrink:0;margin-top:2px;}
.assignment-row .a-text{font-size:13.5px;color:var(--ink);line-height:1.5;}
.assignment-row.done .a-text{color:var(--ink-faint);text-decoration:line-through;}
.locked-box{background:#fff;color:var(--ink);border-radius:16px;padding:60px 30px;text-align:center;}
.locked-box .lock-ico{font-size:42px;margin-bottom:14px;}
.back-link{display:inline-block;margin-bottom:18px;font-family:var(--mono);font-size:12px;color:rgba(255,255,255,0.65);}
.back-link:hover{color:#fff;}

table.admin-table{width:100%;border-collapse:collapse;background:#fff;color:var(--ink);border-radius:14px;overflow:hidden;}
table.admin-table th{text-align:left;font-family:var(--mono);font-size:10.5px;text-transform:uppercase;letter-spacing:0.05em;color:var(--ink-faint);padding:12px 16px;border-bottom:2px solid var(--line);background:var(--card-2);}
table.admin-table td{padding:12px 16px;border-bottom:1px solid var(--line);font-size:13.5px;}
table.admin-table tr:last-child td{border-bottom:none;}
table.admin-table a{color:var(--p2);font-weight:600;}

.creds-box{background:var(--card-2);border:1px solid var(--line);border-radius:12px;padding:20px 24px;margin:18px 0;}
.creds-box .cline{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px;}
.creds-box .cline:last-child{border-bottom:none;}
.creds-box .cline b{font-family:var(--mono);}
"""


def layout(title, body, user=None, wide=False):
    nav = ""
    if user and user["role"] == "student":
        nav = f"""<a href="/dashboard">Dashboard</a><a href="/logout">Logout ({user['username']})</a>"""
    elif user and user["role"] == "admin":
        nav = f"""<a href="/admin">Admin Panel</a><a href="/logout">Logout</a>"""
    else:
        nav = """<a href="/login/student">Student Login</a><a href="/login/admin">Admin Login</a>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — D'TALE Student Portal</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>{BASE_CSS}</style>
</head>
<body>
<div class="topbar wrap">
  <div class="brand"><span class="dot"></span> D'TALE LEARNING CENTER</div>
  <div class="topnav">{nav}</div>
</div>
{body}
</body>
</html>"""


# ---------------------------------------------------------------- auth pages
def render_landing():
    body = """
<div class="center-screen">
  <div>
    <h1 style="text-align:center;color:#fff;font-size:30px;margin-bottom:6px;">120-Day AI Learning Journey</h1>
    <p style="text-align:center;color:rgba(255,255,255,0.6);margin-bottom:30px;font-size:14px;">Choose how you'd like to continue</p>
    <div class="choice-grid">
      <div class="choice-card">
        <div class="ico">🎓</div>
        <h3>Student</h3>
        <p>Log in with the ID and password from your registration PDF, or register for the first time.</p>
        <a class="btn btn-gold" href="/login/student" style="margin-bottom:10px;display:block;">Student Login</a>
        <a class="btn btn-outline" href="/register" style="display:block;">Register</a>
      </div>
      <div class="choice-card">
        <div class="ico">🛠️</div>
        <h3>Admin</h3>
        <p>View every registered student and their progress through all 42 chapters and 10 projects.</p>
        <a class="btn btn-gold" href="/login/admin" style="display:block;">Admin Login</a>
      </div>
    </div>
  </div>
</div>
"""
    return layout("Welcome", body)


def render_admin_login(error):
    err_html = f'<div class="error-box">{error}</div>' if error else ""
    body = f"""
<div class="center-screen">
  <div class="auth-card">
    <h2>Admin Login</h2>
    <div class="sub">D'TALE staff access only.</div>
    {err_html}
    <form method="POST">
      <div class="field"><label>Admin ID</label><input type="text" name="username" required autofocus></div>
      <div class="field"><label>Password</label><input type="password" name="password" required></div>
      <button class="btn btn-gold" type="submit">Log In</button>
    </form>
    <div class="muted-link"><a href="/">← Back</a></div>
  </div>
</div>
"""
    return layout("Admin Login", body)


def render_student_login(error):
    err_html = f'<div class="error-box">{error}</div>' if error else ""
    body = f"""
<div class="center-screen">
  <div class="auth-card">
    <h2>Student Login</h2>
    <div class="sub">Use the ID and password from your registration PDF.</div>
    {err_html}
    <form method="POST">
      <div class="field"><label>Student ID</label><input type="text" name="username" required autofocus></div>
      <div class="field"><label>Password</label><input type="password" name="password" required></div>
      <button class="btn btn-gold" type="submit">Log In</button>
    </form>
    <div class="muted-link">New here? <a href="/register">Register for an account</a></div>
    <div class="muted-link"><a href="/">← Back</a></div>
  </div>
</div>
"""
    return layout("Student Login", body)


def render_register(error):
    err_html = f'<div class="error-box">{error}</div>' if error else ""
    body = f"""
<div class="center-screen">
  <div class="auth-card">
    <h2>Student Registration</h2>
    <div class="sub">We'll generate your login ID and password automatically after this.</div>
    {err_html}
    <form method="POST">
      <div class="field"><label>Full Name</label><input type="text" name="name" required autofocus placeholder="e.g. Riya Sharma"></div>
      <div class="field"><label>Email ID</label><input type="email" name="email" required placeholder="you@example.com"></div>
      <div class="field"><label>Phone Number</label><input type="tel" name="phone" required placeholder="9XXXXXXXXX"></div>
      <button class="btn btn-gold" type="submit">Register</button>
    </form>
    <div class="muted-link"><a href="/">← Back</a></div>
  </div>
</div>
"""
    return layout("Register", body)


def render_register_success(user):
    password = __import__("helpers").generate_password(user["name"])
    body = f"""
<div class="center-screen">
  <div class="auth-card" style="max-width:480px;">
    <h2>You're In, {user['name'].split()[0]}! 🎉</h2>
    <div class="success-box">Registration complete. Your account is ready.</div>
    <div class="creds-box">
      <div class="cline"><span>Student ID</span><b>{user['username']}</b></div>
      <div class="cline"><span>Password</span><b>{password}</b></div>
    </div>
    <p style="font-size:13px;color:var(--ink-dim);margin-bottom:18px;">
      Download your credentials PDF now — your password won't be shown again after you leave this page.
    </p>
    <a class="btn btn-gold" href="/register/pdf/{user['id']}" style="display:block;margin-bottom:10px;">⬇ Download Credentials PDF</a>
    <a class="btn btn-outline" href="/login/student" style="display:block;">Go to Student Login →</a>
  </div>
</div>
"""
    return layout("Registration Complete", body)


# ---------------------------------------------------------------- student dashboard
def render_dashboard(user, chapters, projects, chapter_status, project_status):
    done_chapters = sum(1 for v in chapter_status.values() if v == "done")
    done_projects = sum(1 for v in project_status.values() if v == "done")

    cards = []
    for c in chapters:
        status = chapter_status[c["id"]]
        if status == "locked":
            cards.append(f"""
            <div class="ch-card locked">
              <div class="ch-num">CHAPTER {c['id']:02d}</div>
              <h4>{c['title']}</h4>
              <div class="ch-bar-track"><div class="ch-bar-fill" style="width:0%;"></div></div>
              <div class="ch-foot"><span>0 / 50 done</span><span class="badge-lock">🔒</span></div>
            </div>""")
        else:
            done_count = 50 if status == "done" else _done_count(user["id"], c["id"])
            pct = int(done_count / 50 * 100)
            badge = '<span class="badge-done">DONE</span>' if status == "done" else f'<span style="font-size:11px;">{pct}%</span>'
            cards.append(f"""
            <a class="ch-card-link" href="/chapter/{c['id']}">
              <div class="ch-card">
                <div class="ch-num">CHAPTER {c['id']:02d}</div>
                <h4>{c['title']}</h4>
                <div class="ch-bar-track"><div class="ch-bar-fill" style="width:{pct}%;"></div></div>
                <div class="ch-foot"><span>{done_count} / 50 done</span>{badge}</div>
              </div>
            </a>""")

    proj_cards = []
    for p in projects:
        status = project_status[p["id"]]
        cls = "locked" if status == "locked" else ""
        if status == "locked":
            proj_cards.append(f"""
            <div class="proj-card locked">
              <span class="ptag">Project {p['id']:02d}</span>
              <h4>{p['title']} 🔒</h4>
              <p>{p['tagline']}</p>
            </div>""")
        else:
            tag = "✅ Completed" if status == "done" else p["tagline"]
            proj_cards.append(f"""
            <a class="ch-card-link" href="/project/{p['id']}">
              <div class="proj-card">
                <span class="ptag">Project {p['id']:02d}</span>
                <h4>{p['title']}</h4>
                <p>{tag}</p>
              </div>
            </a>""")

    body = f"""
<div class="page wrap">
  <h1>Welcome back, {user['name'].split()[0]} 👋</h1>
  <div class="sub">Finish all 50 assignments in a chapter to unlock the next one.</div>

  <div class="progress-summary">
    <div class="stat"><b>{done_chapters}/42</b><span>Chapters Done</span></div>
    <div class="stat"><b>{done_projects}/10</b><span>Projects Done</span></div>
    <div class="stat"><b>{int((done_chapters/42)*100)}%</b><span>Curriculum Complete</span></div>
  </div>

  <div class="section-label">📚 Chapters</div>
  <div class="chapter-grid">{''.join(cards)}</div>

  <div class="section-label">🚀 Capstone Projects {'(unlock after all 42 chapters)' if done_chapters < 42 else ''}</div>
  <div class="proj-grid">{''.join(proj_cards)}</div>
</div>
"""
    return layout("Dashboard", body, user=user)


def _done_count(user_id, chapter_id):
    import db
    prog = db.get_chapter_progress(user_id, chapter_id)
    return len(prog["done_indices"])


# ---------------------------------------------------------------- chapter detail
def render_chapter(user, chapter, assignment_list, done_set, locked):
    if locked:
        body = f"""
<div class="page wrap">
  <a class="back-link" href="/dashboard">← Back to Dashboard</a>
  <div class="locked-box">
    <div class="lock-ico">🔒</div>
    <h2>Chapter {chapter['id']:02d} is locked</h2>
    <p style="color:var(--ink-dim);max-width:420px;margin:10px auto 0;">Finish all 50 assignments in the previous chapter to unlock "{chapter['title']}".</p>
  </div>
</div>
"""
        return layout(chapter["title"], body, user=user)

    rows = []
    for i, text in enumerate(assignment_list):
        is_done = i in done_set
        row_cls = "assignment-row done" if is_done else "assignment-row"
        mark = "✓" if is_done else ""
        rows.append(f"""
        <div class="{row_cls}">
          <form method="POST" action="/chapter/{chapter['id']}/toggle/{i}">
            <button class="chk-btn" type="submit">{mark}</button>
          </form>
          <div class="a-num">{i+1:02d}</div>
          <div class="a-text">{text}</div>
        </div>""")

    done_count = len(done_set)
    pct = int(done_count / 50 * 100)

    body = f"""
<div class="page wrap">
  <a class="back-link" href="/dashboard">← Back to Dashboard</a>
  <div class="chapter-detail">
    <div class="ch-head">
      <div>
        <div class="ch-part">{chapter['part']} · Chapter {chapter['id']:02d}</div>
        <h2>{chapter['title']}</h2>
      </div>
      <div class="progress-pill">{done_count} / 50 assignments complete ({pct}%)</div>
    </div>
    <p style="color:var(--ink-dim);font-size:13.5px;">Full notes for this chapter live on the Notes page — these are the 50 practice assignments to actually lock in the learning. Click a circle to mark an assignment done.</p>
    <div class="assignment-list">{''.join(rows)}</div>
  </div>
</div>
"""
    return layout(chapter["title"], body, user=user)


# ---------------------------------------------------------------- project detail
def render_project(user, proj, locked, done):
    if locked:
        body = f"""
<div class="page wrap">
  <a class="back-link" href="/dashboard">← Back to Dashboard</a>
  <div class="locked-box">
    <div class="lock-ico">🔒</div>
    <h2>Project {proj['id']:02d} is locked</h2>
    <p style="color:var(--ink-dim);max-width:420px;margin:10px auto 0;">Complete all 42 chapters (and any earlier projects) to unlock "{proj['title']}".</p>
  </div>
</div>
"""
        return layout(proj["title"], body, user=user)

    deliverables = "".join(f"<li>{d}</li>" for d in proj["deliverables"])
    action = (
        '<div class="success-box">✅ Marked complete. Nice work.</div>'
        if done else
        f'<form method="POST" action="/project/{proj["id"]}/complete"><button class="btn btn-gold" type="submit">Mark This Project Complete</button></form>'
    )
    undo = (
        f'<form method="POST" action="/project/{proj["id"]}/complete" style="margin-top:10px;"><button class="btn btn-outline" type="submit">Undo / Mark Incomplete</button></form>'
        if done else ""
    )

    body = f"""
<div class="page wrap">
  <a class="back-link" href="/dashboard">← Back to Dashboard</a>
  <div class="chapter-detail">
    <div class="ch-part">CAPSTONE PROJECT {proj['id']:02d}</div>
    <h2>{proj['title']}</h2>
    <p style="color:var(--ink-dim);font-size:14px;margin-top:4px;">{proj['tagline']}</p>
    <p style="margin-top:18px;">{proj['brief']}</p>
    <h4 style="margin-top:20px;font-size:14px;">Deliverables</h4>
    <ul style="font-size:13.5px;color:var(--ink-dim);">{deliverables}</ul>
    <h4 style="margin-top:18px;font-size:14px;">Suggested stack</h4>
    <p style="font-size:13.5px;color:var(--ink-dim);">{proj['stack']}</p>
    <h4 style="margin-top:18px;font-size:14px;">Estimated time</h4>
    <p style="font-size:13.5px;color:var(--ink-dim);">{proj['est_time']}</p>
    <div style="margin-top:24px;">{action}{undo}</div>
  </div>
</div>
"""
    return layout(proj["title"], body, user=user)


# ---------------------------------------------------------------- admin
def render_admin_dashboard(user, rows):
    if not rows:
        table = '<p style="color:rgba(255,255,255,0.6);">No students have registered yet.</p>'
    else:
        trs = []
        for r in rows:
            s = r["user"]
            trs.append(f"""
            <tr>
              <td>{s['name']}</td>
              <td>{s['username']}</td>
              <td>{s['email']}</td>
              <td>{s['phone']}</td>
              <td>{r['done_chapters']} / 42</td>
              <td>{r['done_projects']} / 10</td>
              <td><a href="/admin/student/{s['id']}">View →</a></td>
            </tr>""")
        table = f"""
        <table class="admin-table">
          <tr><th>Name</th><th>Student ID</th><th>Email</th><th>Phone</th><th>Chapters</th><th>Projects</th><th></th></tr>
          {''.join(trs)}
        </table>"""

    body = f"""
<div class="page wrap">
  <h1>Admin Panel</h1>
  <div class="sub">{len(rows)} registered student(s)</div>
  {table}
</div>
"""
    return layout("Admin Panel", body, user=user)


def render_admin_student_detail(admin_user, student, chapters, projects, chapter_status, project_status):
    ch_rows = "".join(
        f"<tr><td>Ch. {c['id']:02d} — {c['title']}</td><td>{chapter_status[c['id']].upper()}</td></tr>"
        for c in chapters
    )
    proj_rows = "".join(
        f"<tr><td>Project {p['id']:02d} — {p['title']}</td><td>{project_status[p['id']].upper()}</td></tr>"
        for p in projects
    )
    body = f"""
<div class="page wrap">
  <a class="back-link" href="/admin">← Back to Admin Panel</a>
  <h1>{student['name']}</h1>
  <div class="sub">ID: {student['username']} · {student['email']} · {student['phone']}</div>

  <div class="section-label">Chapters</div>
  <table class="admin-table">{ch_rows}</table>

  <div class="section-label">Projects</div>
  <table class="admin-table">{proj_rows}</table>
</div>
"""
    return layout(f"{student['name']} — Progress", body, user=admin_user)
