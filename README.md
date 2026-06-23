# D'TALE Student Portal

A self-contained Flask app: admin + student login, student self-registration
with auto-generated credentials (delivered as a PDF), 42 chapters x 50
assignments each, 10 capstone projects, and progress-gated unlocking.

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000**

A file called `dtale_portal.db` (SQLite) is created automatically on first
run, in the same folder, and stores every account and every bit of progress.
Delete that file to reset the whole portal back to empty.

## Logging in

**Admin**
- ID: `Arabinda`
- Password: `Arabinda123`

**Students** register themselves from the landing page with name, email, and
phone. The portal then generates:
- **Student ID** = first name, lowercase (e.g. `riya`; a second "Riya" would
  automatically become `riya2`, and so on)
- **Password** = `FirstName@123` (e.g. `Riya@123`)

Both are shown once on screen and on a downloadable PDF — the password is
**not** stored anywhere in plaintext (it's hashed in the database, the same
way the admin password is), so if a student loses the PDF, an admin would
need to register them again or you'd add a "reset password" feature.

## How the gating works

- Chapter 1 is unlocked for every new student.
- A chapter is marked complete only when **all 50** of its assignments are
  checked off.
- Completing chapter *N* unlocks chapter *N+1*. Chapters 2–42 stay locked
  (visibly, with a 🔒) until then.
- All 10 capstone projects stay locked until **all 42 chapters** are done.
  Completing project *N* unlocks project *N+1*.

## Where the 2,100 assignments come from

Hand-writing 50 truly distinct assignments for each of 42 chapters
(2,100 total) isn't something to type out by hand reliably — instead,
`assignments.py` generates them deterministically from `data.py`, which
gives each chapter exactly 10 keywords pulled from your chapter content,
combined with a bank of question templates (explain it, try it, build it,
break it, quiz yourself, etc.). The same chapter always produces the same
50 assignments in the same order, so a student's checked-off progress never
gets scrambled by a restart.

If you want to hand-edit any chapter's assignments later, the cleanest way
is to override its keyword list in `data.py` — the wording will follow
automatically.

## File map

| File | What it does |
|---|---|
| `app.py` | Flask routes: auth, registration, dashboard, chapter/project pages, admin views |
| `db.py` | SQLite schema + all reads/writes (users, chapter progress, project progress) |
| `data.py` | The 42 chapters (title, part, type, 10 keywords each) and the 10 projects |
| `assignments.py` | Turns a chapter's 10 keywords into 50 assignment strings |
| `helpers.py` | Username/password generation from a student's name |
| `credentials_pdf.py` | Builds the one-page PDF handed to a student after registration |
| `templates.py` | All HTML for every page, as Python strings |

## Moving this to production

This ships with Flask's built-in dev server (`debug=True`), which is fine for
trying it out or running it on your own machine, but isn't meant for the
public internet. Before putting it on a real domain:
- Run it behind a real WSGI server (gunicorn, waitress) instead of `app.run()`
- Set `DTALE_SECRET_KEY` to a long random value as an environment variable
  instead of using the default in `app.py`
- Consider moving from SQLite to Postgres if you expect more than a
  handful of concurrent students
