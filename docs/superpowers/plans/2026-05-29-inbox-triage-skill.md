# Inbox Triage Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `/triage` skill that reads Gmail, classifies mail by Paul's Email Profile, drafts replies in his voice into Gmail Drafts, and logs measurable time saved.

**Architecture:** Hybrid. A `/triage` prompt-skill owns classification + voice drafting; tested Python utilities in `actions/triage/` own the mechanical parts (noise pre-filter, candidate loading, Gmail draft creation, run logging). Data lives in the existing `reach/data/intel.db`.

**Tech Stack:** Python 3.14, pytest 9.0.3 (already installed), google-api-python-client / google-auth (already installed), SQLite (stdlib), Gmail API (`gmail.readonly` + `gmail.compose`).

---

## File Structure

**Create:**
- `actions/__init__.py` — make `actions` an importable package (empty).
- `actions/triage/__init__.py` — package marker (empty).
- `actions/triage/prefilter.py` — deterministic noise pre-filter.
- `actions/triage/runlog.py` — run logging + weekly rollup.
- `actions/triage/gmail_draft.py` — MIME reply builder + Gmail draft creation + service helper.
- `actions/triage/emails.py` — candidate loader (DB read + optional refresh).
- `.claude/commands/triage.md` — the orchestrator skill.
- `conftest.py` — repo-root pytest config (puts repo root on `sys.path`).
- `tests/triage/test_prefilter.py`
- `tests/triage/test_runlog.py`
- `tests/triage/test_gmail_draft.py`
- `tests/triage/test_emails.py`
- `tuning/triage/` — created at runtime by `runlog` (the human-readable log lands here).

**Modify:**
- `reach/collectors/db.py` — add `thread_id` to `emails`; add `triage_actions` and `triage_runs` tables.
- `reach/collectors/gmail.py` — store `thread_id` on insert.
- `reach/auth/gmail_auth.py` — widen scopes to `gmail.readonly` + `gmail.compose`.

---

## Task 1: Test harness setup

**Files:**
- Create: `conftest.py`
- Create: `actions/__init__.py`, `actions/triage/__init__.py`
- Create: `tests/triage/test_smoke.py` (temporary, deleted at end of task)

- [ ] **Step 1: Create the package markers and conftest**

Create `conftest.py` (repo root):
```python
import sys
from pathlib import Path

# Put the repo root on sys.path so `import actions.triage.*` works in tests.
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
```

Create empty `actions/__init__.py` and `actions/triage/__init__.py` (zero bytes each).

- [ ] **Step 2: Write a smoke test**

Create `tests/triage/test_smoke.py`:
```python
def test_smoke():
    import actions.triage  # noqa: F401
    assert True
```

- [ ] **Step 3: Run it**

Run: `python -m pytest tests/triage/test_smoke.py -v`
Expected: PASS (confirms import path + pytest work).

- [ ] **Step 4: Delete the smoke test and commit**

```bash
rm tests/triage/test_smoke.py
git add conftest.py actions/__init__.py actions/triage/__init__.py
git commit -m "test: scaffold actions.triage package and pytest path"
```

---

## Task 2: Database schema (thread_id + triage tables)

**Files:**
- Modify: `reach/collectors/db.py`
- Test: `tests/triage/test_db_schema.py`

- [ ] **Step 1: Write the failing test**

Create `tests/triage/test_db_schema.py`:
```python
import sqlite3
import importlib.util
from pathlib import Path

DB_MODULE = Path(__file__).resolve().parents[2] / "reach" / "collectors" / "db.py"

def _load_db_module():
    spec = importlib.util.spec_from_file_location("aios_db", DB_MODULE)
    mod = importlib.util.module_from_spec(spec)
    # db.py imports `from config import ...`; add its dir to path first.
    import sys
    sys.path.insert(0, str(DB_MODULE.parent))
    spec.loader.exec_module(mod)
    return mod

def test_intel_schema_has_thread_id_and_triage_tables(tmp_path, monkeypatch):
    db = _load_db_module()
    intel = tmp_path / "intel.db"
    monkeypatch.setattr(db, "INTEL_DB_PATH", str(intel))
    db.init_intel_db()

    conn = sqlite3.connect(str(intel))
    cols = {r[1] for r in conn.execute("PRAGMA table_info(emails)")}
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()

    assert "thread_id" in cols
    assert "triage_actions" in tables
    assert "triage_runs" in tables
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/triage/test_db_schema.py -v`
Expected: FAIL (`thread_id` not in cols; triage tables missing).

- [ ] **Step 3: Edit `reach/collectors/db.py`**

In `init_intel_db()`, change the `emails` table definition to add `thread_id TEXT` (after `message_id`), and append two new tables inside the same `executescript`:

```python
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            message_id TEXT UNIQUE,
            thread_id TEXT,
            date TEXT,
            sender TEXT,
            subject TEXT,
            body_preview TEXT,
            labels TEXT,
            collected_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS triage_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT UNIQUE,
            classification TEXT,
            action TEXT,
            draft_id TEXT,
            run_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS triage_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date TEXT NOT NULL,
            seen INTEGER,
            drafted INTEGER,
            surfaced INTEGER,
            ignored INTEGER,
            est_minutes_saved INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
```

(Leave the existing `meetings` table as-is.)

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/triage/test_db_schema.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add reach/collectors/db.py tests/triage/test_db_schema.py
git commit -m "feat: add thread_id and triage tables to intel.db schema"
```

---

## Task 3: Noise pre-filter

**Files:**
- Create: `actions/triage/prefilter.py`
- Test: `tests/triage/test_prefilter.py`

- [ ] **Step 1: Write the failing test**

Create `tests/triage/test_prefilter.py`:
```python
import pytest
from actions.triage.prefilter import prefilter

@pytest.mark.parametrize("sender,subject,expected", [
    ("noreply@github.com", "Your PR was merged", "ignore"),
    ("no-reply@accounts.google.com", "Security alert", "ignore"),
    ("lbbw-jobnotification@noreply12.jobs2web.com", "Neue Stellen", "ignore"),
    ("hello@students.udemy.com", "Your weekly digest", "ignore"),
    ("billing@stripe.com", "Your receipt from Acme", "ignore"),
    ("Emma Jacobs <emma@stepstone.de>", "Re: AI Engineer role", "candidate"),
    ("Paulina <paulina@eraneos.com>", "Following up on your application", "candidate"),
    ("jane@somestartup.io", "Question about a pilot project", "candidate"),
])
def test_prefilter(sender, subject, expected):
    assert prefilter(sender, subject) == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/triage/test_prefilter.py -v`
Expected: FAIL (`ModuleNotFoundError: actions.triage.prefilter`).

- [ ] **Step 3: Write minimal implementation**

Create `actions/triage/prefilter.py`:
```python
"""Deterministic noise pre-filter. The nuanced ignore/draft/gray-zone
decision is made by the model in the /triage skill; this only drops
obvious machine noise so the model reviews fewer items."""

NOISE_SENDER_FRAGMENTS = (
    "noreply@", "no-reply@", "donotreply@", "do-not-reply@",
    "notifications@", "notification@", "mailer@", "mailer-daemon@",
    "bounce@", "bounces@", "noreply12.", "jobnotification@",
)

NOISE_SUBJECT_FRAGMENTS = (
    "unsubscribe", "newsletter", "digest", "weekly roundup",
    "your receipt", "receipt from", "invoice #", "order confirmation",
    "security alert", "verify your email",
)


def prefilter(sender: str, subject: str) -> str:
    """Return "ignore" for obvious machine noise, else "candidate"."""
    s = (sender or "").lower()
    sub = (subject or "").lower()
    if any(frag in s for frag in NOISE_SENDER_FRAGMENTS):
        return "ignore"
    if any(frag in sub for frag in NOISE_SUBJECT_FRAGMENTS):
        return "ignore"
    return "candidate"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/triage/test_prefilter.py -v`
Expected: PASS (8 passed).

- [ ] **Step 5: Commit**

```bash
git add actions/triage/prefilter.py tests/triage/test_prefilter.py
git commit -m "feat: add deterministic noise pre-filter for triage"
```

---

## Task 4: Run logging + weekly rollup

**Files:**
- Create: `actions/triage/runlog.py`
- Test: `tests/triage/test_runlog.py`

- [ ] **Step 1: Write the failing test**

Create `tests/triage/test_runlog.py`:
```python
import sqlite3
import datetime
from actions.triage import runlog

def _make_runs_table(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE triage_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date TEXT NOT NULL, seen INTEGER, drafted INTEGER,
            surfaced INTEGER, ignored INTEGER, est_minutes_saved INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)
    """)
    conn.commit(); conn.close()

def test_record_run_inserts_and_estimates(tmp_path):
    db = tmp_path / "intel.db"; _make_runs_table(str(db))
    log = tmp_path / "log.md"
    est = runlog.record_run(seen=10, drafted=3, surfaced=1, ignored=6,
                            run_date="2026-05-29", db_path=str(db), log_path=str(log))
    assert est == 3 * runlog.MINUTES_PER_DRAFT
    conn = sqlite3.connect(str(db))
    row = conn.execute("SELECT seen, drafted, est_minutes_saved FROM triage_runs").fetchone()
    conn.close()
    assert row == (10, 3, 3 * runlog.MINUTES_PER_DRAFT)
    assert log.exists() and "2026-05-29" in log.read_text()

def test_weekly_rollup_sums_last_7_days(tmp_path):
    db = tmp_path / "intel.db"; _make_runs_table(str(db))
    today = datetime.date(2026, 5, 29)
    # in-window (today and 6 days ago) and out-of-window (7 days ago)
    runlog.record_run(5, 2, 0, 3, run_date="2026-05-29", db_path=str(db), log_path=str(tmp_path/"l.md"))
    runlog.record_run(5, 1, 0, 4, run_date="2026-05-23", db_path=str(db), log_path=str(tmp_path/"l.md"))
    runlog.record_run(5, 9, 0, 0, run_date="2026-05-22", db_path=str(db), log_path=str(tmp_path/"l.md"))
    r = runlog.weekly_rollup(db_path=str(db), today=today)
    assert r["drafts"] == 3            # 2 + 1, excludes the 22nd
    assert r["minutes"] == 3 * runlog.MINUTES_PER_DRAFT
    assert r["runs"] == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/triage/test_runlog.py -v`
Expected: FAIL (`ModuleNotFoundError: actions.triage.runlog`).

- [ ] **Step 3: Write minimal implementation**

Create `actions/triage/runlog.py`:
```python
"""Records each triage run and computes the weekly time-saved rollup."""
import sqlite3
import datetime
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = str(_ROOT / "reach" / "data" / "intel.db")
DEFAULT_LOG_PATH = str(_ROOT / "tuning" / "triage" / "log.md")
MINUTES_PER_DRAFT = 6  # tunable estimate of minutes saved per drafted reply


def record_run(seen, drafted, surfaced, ignored, run_date=None,
               db_path=DEFAULT_DB_PATH, log_path=DEFAULT_LOG_PATH):
    run_date = run_date or datetime.date.today().isoformat()
    est = drafted * MINUTES_PER_DRAFT
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO triage_runs (run_date, seen, drafted, surfaced, ignored, est_minutes_saved)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        (run_date, seen, drafted, surfaced, ignored, est),
    )
    conn.commit(); conn.close()
    _append_log(run_date, seen, drafted, surfaced, est, log_path)
    return est


def weekly_rollup(db_path=DEFAULT_DB_PATH, today=None):
    today = today or datetime.date.today()
    since = (today - datetime.timedelta(days=6)).isoformat()
    conn = sqlite3.connect(db_path); conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT COALESCE(SUM(drafted),0) AS d, COALESCE(SUM(est_minutes_saved),0) AS m,"
        " COUNT(*) AS runs FROM triage_runs WHERE run_date >= ?",
        (since,),
    ).fetchone()
    conn.close()
    return {"since": since, "drafts": row["d"], "minutes": row["m"], "runs": row["runs"]}


def _append_log(run_date, seen, drafted, surfaced, est, log_path):
    p = Path(log_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("# Triage Log\n\n| Date | Seen | Drafted | Surfaced | Est. min saved |\n"
                     "|------|------|---------|----------|----------------|\n", encoding="utf-8")
    with p.open("a", encoding="utf-8") as f:
        f.write(f"| {run_date} | {seen} | {drafted} | {surfaced} | {est} |\n")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/triage/test_runlog.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add actions/triage/runlog.py tests/triage/test_runlog.py
git commit -m "feat: add triage run logging and weekly rollup"
```

---

## Task 5: Gmail draft builder + creation

**Files:**
- Create: `actions/triage/gmail_draft.py`
- Test: `tests/triage/test_gmail_draft.py`

- [ ] **Step 1: Write the failing test**

Create `tests/triage/test_gmail_draft.py`:
```python
import base64
from actions.triage import gmail_draft

def test_build_reply_mime_adds_re_prefix():
    msg = gmail_draft.build_reply_mime("a@b.com", "Interview times", "Sounds good.\nPaul")
    assert msg["Subject"] == "Re: Interview times"
    assert msg["To"] == "a@b.com"
    assert "Sounds good." in msg.get_content()

def test_build_reply_mime_keeps_existing_re():
    msg = gmail_draft.build_reply_mime("a@b.com", "Re: Interview times", "ok")
    assert msg["Subject"] == "Re: Interview times"

def test_build_reply_mime_sets_threading_headers():
    msg = gmail_draft.build_reply_mime("a@b.com", "Hi", "ok", in_reply_to="<abc@mail>")
    assert msg["In-Reply-To"] == "<abc@mail>"
    assert msg["References"] == "<abc@mail>"

def test_create_reply_draft_calls_api_with_thread_and_raw():
    calls = {}
    class FakeDrafts:
        def create(self, userId, body):
            calls["userId"] = userId; calls["body"] = body
            class E:  # noqa
                def execute(self_inner):
                    return {"id": "draft123"}
            return E()
    class FakeUsers:
        def drafts(self): return FakeDrafts()
    class FakeService:
        def users(self): return FakeUsers()

    draft_id = gmail_draft.create_reply_draft(
        FakeService(), thread_id="T1", to="a@b.com", subject="Hi",
        body="ok", in_reply_to="<abc@mail>")
    assert draft_id == "draft123"
    assert calls["body"]["message"]["threadId"] == "T1"
    raw = calls["body"]["message"]["raw"]
    decoded = base64.urlsafe_b64decode(raw).decode()
    assert "To: a@b.com" in decoded
    assert "Re: Hi" in decoded
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/triage/test_gmail_draft.py -v`
Expected: FAIL (`ModuleNotFoundError: actions.triage.gmail_draft`).

- [ ] **Step 3: Write minimal implementation**

Create `actions/triage/gmail_draft.py`:
```python
"""Builds threaded plain-text reply MIME and creates Gmail drafts.
Requires a token with the gmail.compose scope. Never sends — only creates drafts."""
import base64
from email.message import EmailMessage
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TOKEN_PATH = str(_ROOT / "reach" / "auth" / "token.json")


def build_reply_mime(to, subject, body, in_reply_to=None, references=None):
    msg = EmailMessage()
    msg["To"] = to
    subject = subject or ""
    msg["Subject"] = subject if subject.lower().startswith("re:") else f"Re: {subject}"
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = references or in_reply_to
    msg.set_content(body)
    return msg


def _encode(msg):
    return base64.urlsafe_b64encode(msg.as_bytes()).decode()


def create_reply_draft(service, thread_id, to, subject, body,
                       in_reply_to=None, references=None):
    msg = build_reply_mime(to, subject, body, in_reply_to, references)
    body_obj = {"message": {"raw": _encode(msg), "threadId": thread_id}}
    draft = service.users().drafts().create(userId="me", body=body_obj).execute()
    return draft["id"]


def get_gmail_service(token_path=DEFAULT_TOKEN_PATH):
    """Build a Gmail API service from the saved token (lazy imports so tests
    that only exercise the pure builders don't need google libs)."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_file(str(token_path))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        Path(token_path).write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/triage/test_gmail_draft.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add actions/triage/gmail_draft.py tests/triage/test_gmail_draft.py
git commit -m "feat: add Gmail reply MIME builder and draft creation"
```

---

## Task 6: Candidate loader

**Files:**
- Create: `actions/triage/emails.py`
- Test: `tests/triage/test_emails.py`

- [ ] **Step 1: Write the failing test**

Create `tests/triage/test_emails.py`:
```python
import sqlite3
from actions.triage import emails

def _seed(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("""CREATE TABLE emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT, message_id TEXT UNIQUE,
        thread_id TEXT, date TEXT, sender TEXT, subject TEXT, body_preview TEXT,
        labels TEXT, collected_at TEXT)""")
    conn.execute("""CREATE TABLE triage_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, message_id TEXT UNIQUE, classification TEXT,
        action TEXT, draft_id TEXT, run_date TEXT, created_at TEXT)""")
    rows = [
        ("gmail", "<m1>", "T1", "2026-05-29", "Paulina <p@eraneos.com>", "Re: your application", "hi", ""),
        ("gmail", "<m2>", "T2", "2026-05-29", "noreply@github.com", "PR merged", "x", ""),
        ("gmail", "<m3>", "T3", "2026-05-29", "Recruiter <r@firm.com>", "AI role", "y", ""),
    ]
    conn.executemany("INSERT INTO emails (source,message_id,thread_id,date,sender,subject,body_preview,labels)"
                     " VALUES (?,?,?,?,?,?,?,?)", rows)
    # m3 already triaged -> must be excluded
    conn.execute("INSERT INTO triage_actions (message_id, action) VALUES ('<m3>', 'drafted')")
    conn.commit(); conn.close()

def test_read_candidates_excludes_noise_and_already_triaged(tmp_path):
    db = tmp_path / "intel.db"; _seed(str(db))
    cands = emails.read_candidates(db_path=str(db))
    ids = {c["message_id"] for c in cands}
    assert ids == {"<m1>"}              # m2 noise-filtered, m3 already triaged
    assert cands[0]["thread_id"] == "T1"
    assert cands[0]["sender"] == "Paulina <p@eraneos.com>"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/triage/test_emails.py -v`
Expected: FAIL (`ModuleNotFoundError: actions.triage.emails`).

- [ ] **Step 3: Write minimal implementation**

Create `actions/triage/emails.py`:
```python
"""Loads triage candidates from intel.db. Optionally refreshes the inbox
first by running the existing Gmail collector as a subprocess."""
import sqlite3
import subprocess
import sys
from pathlib import Path

from actions.triage.prefilter import prefilter

_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = str(_ROOT / "reach" / "data" / "intel.db")


def read_candidates(db_path=DEFAULT_DB_PATH, days_back=7):
    conn = sqlite3.connect(db_path); conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT message_id, thread_id, date, sender, subject, body_preview "
        "FROM emails "
        "WHERE message_id NOT IN (SELECT message_id FROM triage_actions) "
        "ORDER BY id DESC"
    ).fetchall()
    conn.close()
    candidates = []
    for r in rows:
        if prefilter(r["sender"], r["subject"]) == "ignore":
            continue
        candidates.append(dict(r))
    return candidates


def refresh_inbox():
    """Run the existing Gmail collector to pull the latest inbox into intel.db.
    Returns True on success, False on failure (caller decides whether to continue)."""
    try:
        subprocess.run([sys.executable, "reach/collectors/gmail.py"],
                       cwd=str(_ROOT), check=True, capture_output=True, timeout=120)
        return True
    except Exception:
        return False


def get_candidates(db_path=DEFAULT_DB_PATH, refresh=True):
    refreshed = refresh_inbox() if refresh else None
    return read_candidates(db_path=db_path), refreshed
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/triage/test_emails.py -v`
Expected: PASS (1 passed).

- [ ] **Step 5: Run the full suite**

Run: `python -m pytest tests/triage -v`
Expected: ALL PASS.

- [ ] **Step 6: Commit**

```bash
git add actions/triage/emails.py tests/triage/test_emails.py
git commit -m "feat: add triage candidate loader with refresh"
```

---

## Task 7: Collector stores thread_id + migrate existing DB

**Files:**
- Modify: `reach/collectors/gmail.py`
- Test: `tests/triage/test_collector_threadid.py`

- [ ] **Step 1: Write the failing test**

Create `tests/triage/test_collector_threadid.py`:
```python
import re
from pathlib import Path

GMAIL = Path(__file__).resolve().parents[2] / "reach" / "collectors" / "gmail.py"

def test_collector_inserts_thread_id():
    src = GMAIL.read_text(encoding="utf-8")
    # The INSERT must include the thread_id column and pull msg["threadId"].
    assert "thread_id" in src
    assert re.search(r'msg\.get\(\s*["\']threadId["\']', src) or 'msg["threadId"]' in src
    # thread_id column present in the INSERT column list
    assert re.search(r"INSERT OR IGNORE INTO emails[\s\S]*thread_id", src)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/triage/test_collector_threadid.py -v`
Expected: FAIL (collector does not reference thread_id yet).

- [ ] **Step 3: Edit `reach/collectors/gmail.py`**

Inside the `for msg_ref in messages:` loop, after `message_id = headers.get(...)`, add:
```python
        thread_id = msg.get("threadId", "")
```
Then replace the existing `INSERT OR IGNORE` block with:
```python
        try:
            c.execute("""
                INSERT OR IGNORE INTO emails
                (source, message_id, thread_id, date, sender, subject, body_preview, labels)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, ("gmail", message_id, thread_id, date_str, sender, subject, body_preview, labels))
            saved += 1
        except Exception:
            pass
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/triage/test_collector_threadid.py -v`
Expected: PASS.

- [ ] **Step 5: Migrate the existing intel.db and backfill**

The live `intel.db` predates the `thread_id` column. Add it (ignore error if it already exists), then re-run the collector to backfill recent mail:
```bash
python -c "import sqlite3; c=sqlite3.connect('reach/data/intel.db'); \
[c.execute(s) for s in ['ALTER TABLE emails ADD COLUMN thread_id TEXT']]; \
c.commit(); print('migrated')" || echo "column already exists"
python reach/collectors/gmail.py
```
Expected: "migrated" (or "column already exists"), then `Gmail: N emails saved...`.

- [ ] **Step 6: Commit**

```bash
git add reach/collectors/gmail.py tests/triage/test_collector_threadid.py
git commit -m "feat: store gmail thread_id for reply threading"
```

---

## Task 8: Widen Gmail OAuth scope (compose) and re-auth

**Files:**
- Modify: `reach/auth/gmail_auth.py`

- [ ] **Step 1: Edit the scopes**

In `reach/auth/gmail_auth.py`, change:
```python
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
```
to:
```python
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]
```

- [ ] **Step 2: Delete the old token and re-authorize**

The existing `token.json` only has `gmail.readonly`. Delete it and re-run auth (a browser opens; approve read-only + compose):
```bash
rm reach/auth/token.json
python reach/auth/gmail_auth.py
```
Expected: browser consent (now lists "Manage drafts and send email"), then `Gmail authorized. Token saved to ...`.

- [ ] **Step 3: Verify the new scopes (no secrets printed)**

Run:
```bash
python -c "import json; d=json.load(open('reach/auth/token.json')); print('scopes:', d.get('scopes'))"
```
Expected: a list containing both `.../gmail.readonly` and `.../gmail.compose`.

- [ ] **Step 4: Commit**

```bash
git add reach/auth/gmail_auth.py
git commit -m "feat: widen gmail scope to compose for draft creation"
```
(`token.json` is gitignored and is not committed.)

---

## Task 9: The `/triage` skill

**Files:**
- Create: `.claude/commands/triage.md`

- [ ] **Step 1: Write the skill file**

Create `.claude/commands/triage.md`:
````markdown
---
name: triage
description: Read Gmail, classify by the CLAUDE.md Email Profile, draft replies in Paul's voice into Gmail Drafts for review, and log time saved. Usage: /triage
user_invocable: true
trigger: /triage
version: 1.0.0
---

# /triage — Inbox Triage

## Step 1: Preconditions

Confirm `reach/auth/token.json` exists and its scopes include `gmail.compose`:
```bash
python -c "import json,sys; d=json.load(open('reach/auth/token.json')); sys.exit(0 if any('gmail.compose' in s for s in d.get('scopes',[])) else 1)" && echo "compose OK" || echo "NEEDS REAUTH"
```
If it prints `NEEDS REAUTH` or the file is missing, stop and tell the user:
"Gmail needs re-auth with compose scope. Run: `rm reach/auth/token.json && python reach/auth/gmail_auth.py`"

## Step 2: Load candidates (refresh first)

Run a Python snippet that refreshes the inbox and loads candidates:
```bash
python -c "import json; from actions.triage.emails import get_candidates; \
cands, refreshed = get_candidates(refresh=True); \
print('REFRESHED', refreshed); print(json.dumps(cands, ensure_ascii=False))"
```
- `REFRESHED False` means the live pull failed — continue on existing data and note it in your summary.
- Parse the JSON list of candidates (each: message_id, thread_id, date, sender, subject, body_preview).
- If the list is empty: report "Inbox clean, nothing to draft," still record a zero run (Step 6), and stop.

## Step 3: Classify each candidate

Apply the **Email Profile in `CLAUDE.md`** to each candidate. Assign exactly one:
- **ignore** — slipped past the pre-filter but is still noise per the profile.
- **gray-zone** — negotiations, declines, rejections, salary discussions, or anything sensitive. NEVER draft these.
- **draft** — any real human with a genuine purpose (recruiters, hiring managers, interview scheduling, application follow-ups, prospective clients, direct questions).

When unsure between draft and gray-zone, choose **gray-zone** (safer — Paul writes it himself).

## Step 4: Draft replies (for "draft" items only)

For each **draft** item, write a reply in Paul's voice using `context/voice/samples.md`:
- Warm and conversational, tight short sentences, polite not formal.
- Obey the banned-words list (no em dashes, no "delve into", "leverage", "robust", etc.).
- Sign-off: "Kind regards, Paul" for recruiters/hiring managers/clients; "Paul" for casual.
- Keep it short. Only address what the email actually asks.

## Step 5: Review table (approval gate)

Present ONE table to Paul and STOP for his decision. Do not create any drafts yet.

| # | From | Subject | Class | Action | Draft preview |
|---|------|---------|-------|--------|---------------|
| 1 | Paulina (Eraneos) | Re: your application | draft | will draft | "Hi Paulina, thanks for..." |
| 2 | Recruiter X | Salary expectations? | gray-zone | you write this | (sensitive — surfaced only) |

Ask: "Approve all drafts, pick numbers, edit any, or skip?" Wait for his answer.

## Step 6: Execute approved drafts + log

For each APPROVED draft, create the Gmail draft and record the action:
```bash
python -c "
import json, datetime
from actions.triage.gmail_draft import get_gmail_service, create_reply_draft
import sqlite3
svc = get_gmail_service()
# ITEMS is a JSON list of {thread_id,to,subject,body,in_reply_to} you fill in:
ITEMS = json.loads('''<JSON_HERE>''')
conn = sqlite3.connect('reach/data/intel.db')
for it in ITEMS:
    did = create_reply_draft(svc, it['thread_id'], it['to'], it['subject'], it['body'], it.get('in_reply_to'))
    conn.execute('INSERT OR IGNORE INTO triage_actions (message_id, classification, action, draft_id, run_date) VALUES (?,?,?,?,?)',
                 (it['message_id'], 'draft', 'drafted', did, datetime.date.today().isoformat()))
conn.commit(); conn.close(); print('drafts created:', len(ITEMS))
"
```
- Use the candidate's `message_id` as `in_reply_to` (it is the RFC Message-ID) and `to` = the candidate's sender.
- Also record `triage_actions` rows for ignore and gray-zone items (action = 'ignored' / 'surfaced', draft_id = NULL) so they are not re-processed next run. Do this with a similar INSERT.
- If a single draft creation raises, report which one failed and continue the rest.

Then record the run and print the rollup:
```bash
python -c "from actions.triage.runlog import record_run, weekly_rollup; \
record_run(seen=SEEN, drafted=DRAFTED, surfaced=SURFACED, ignored=IGNORED); \
import json; print(json.dumps(weekly_rollup()))"
```
(Substitute the integer counts from this run.)

## Step 7: Summary

Print a short summary: drafts created (with where to find them — Gmail Drafts), gray-zone items surfaced (so Paul writes them), and the weekly rollup ("This week: N drafts, ~M minutes saved"). Keep it tight.
````

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/triage.md
git commit -m "feat: add /triage inbox triage skill"
```

---

## Task 10: End-to-end validation

**Files:** none (validation only)

- [ ] **Step 1: Full test suite green**

Run: `python -m pytest tests/triage -v`
Expected: ALL PASS.

- [ ] **Step 2: Dry candidate load against the live DB**

Run:
```bash
python -c "from actions.triage.emails import read_candidates; c=read_candidates(); print('candidates:', len(c)); [print(' -', x['sender'][:40], '|', x['subject'][:45]) for x in c[:8]]"
```
Expected: a list of real human candidates (recruiter/job mail), noise excluded.

- [ ] **Step 3: First real `/triage` run**

In Claude Code, run `/triage`. Verify:
- It refreshes, classifies, and shows the review table.
- On approval, drafts appear in Gmail → Drafts, threaded to the originals.
- Gray-zone items are surfaced, not drafted.
- The weekly rollup prints.

- [ ] **Step 4: Confirm drafts in Gmail**

Open Gmail → Drafts. Confirm the approved replies are there, in the right threads, in Paul's voice, nothing sent.

- [ ] **Step 5: Commit any log output**

```bash
git add tuning/triage/log.md
git commit -m "chore: first triage run log"
```
(`intel.db` is gitignored and stays local.)

---

## Self-Review Notes

- **Spec coverage:** output→Gmail drafts (Tasks 5, 9); all-Draft-bucket coverage + gray-zone surfacing (Task 9 classification); measurement per-run + weekly rollup (Task 4, 9); manual trigger (Task 9 skill); auth/compose change (Task 8); thread_id gap fix (Tasks 2, 7); data model (Task 2); error handling = fail-loud (Task 9 Steps 1, 2, 6); testing on mechanical units (Tasks 3–6). All spec sections map to tasks.
- **Out of scope** (auto-send, scheduling, acceptance tracking, non-Gmail, HTML) is not implemented, per spec.
- **Type/name consistency:** `prefilter()`, `read_candidates()/get_candidates()`, `record_run()/weekly_rollup()/MINUTES_PER_DRAFT`, `build_reply_mime()/create_reply_draft()/get_gmail_service()` are referenced consistently across tasks and the skill.
