import sqlite3
from actions.triage import auto


def _make_tables(db_path):
    conn = sqlite3.connect(db_path)
    conn.executescript("""
        CREATE TABLE triage_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, message_id TEXT UNIQUE,
            classification TEXT, action TEXT, draft_id TEXT, run_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE triage_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, run_date TEXT NOT NULL,
            seen INTEGER, drafted INTEGER, surfaced INTEGER, ignored INTEGER,
            est_minutes_saved INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
    """)
    conn.commit(); conn.close()


def _cand(mid, subject="S", sender="a@b.com"):
    return {"message_id": mid, "thread_id": "t" + mid, "date": "d",
            "sender": sender, "subject": subject, "body_preview": "body"}


# ---- parse_classification ----

def test_parse_classification_draft():
    out = auto.parse_classification('{"classification": "draft", "draft_body": "Hi Lena,\\nthanks."}')
    assert out["classification"] == "draft"
    assert "thanks" in out["draft_body"]

def test_parse_classification_ignore_has_no_body():
    out = auto.parse_classification('{"classification": "ignore", "draft_body": ""}')
    assert out["classification"] == "ignore"
    assert not out["draft_body"]

def test_parse_classification_strips_code_fence():
    out = auto.parse_classification('```json\n{"classification": "gray-zone", "draft_body": ""}\n```')
    assert out["classification"] == "gray-zone"


# ---- build_system_prompt ----

def test_build_system_prompt_embeds_rules_and_voice():
    p = auto.build_system_prompt("PROFILE: ignore newsletters; draft recruiters; gray-zone salary",
                                 "VOICE: no em dashes, sign off Paul")
    low = p.lower()
    assert "ignore" in low and "draft" in low and "gray-zone" in low
    assert "PROFILE:" in p and "VOICE:" in p
    assert "classification" in low  # instructs the JSON output shape


# ---- run_auto_triage ----

def test_run_auto_triage_routes_records_and_summarizes(tmp_path):
    db = tmp_path / "intel.db"; _make_tables(str(db))
    cands = [_cand("m1", "Recruiter role"), _cand("m2", "Salary expectations"), _cand("m3", "Newsletter")]
    verdicts = {
        "m1": {"classification": "draft", "draft_body": "Hi, glad to talk."},
        "m2": {"classification": "gray-zone", "draft_body": ""},
        "m3": {"classification": "ignore", "draft_body": ""},
    }
    reply_calls, summary_calls = [], []
    def make_reply(thread_id, to, subject, body, in_reply_to):
        reply_calls.append((thread_id, to, subject, body, in_reply_to)); return "draft-1"
    def make_summary(to, subject, body):
        summary_calls.append((to, subject, body)); return "summary-1"

    res = auto.run_auto_triage(cands, lambda c: verdicts[c["message_id"]],
                               make_reply, make_summary, self_email="paul@x.com",
                               db_path=str(db), log_path=str(tmp_path / "log.md"), today="2026-05-30")

    assert res == {"seen": 3, "drafted": 1, "surfaced": 1, "ignored": 1, "summary_draft_id": "summary-1"}
    assert len(reply_calls) == 1 and reply_calls[0][4] == "m1"  # in_reply_to = message_id
    assert len(summary_calls) == 1
    conn = sqlite3.connect(str(db))
    rows = dict(conn.execute("SELECT message_id, action FROM triage_actions").fetchall())
    run = conn.execute("SELECT seen, drafted, surfaced, ignored FROM triage_runs").fetchone()
    conn.close()
    assert rows == {"m1": "drafted", "m2": "surfaced", "m3": "ignored"}
    assert run == (3, 1, 1, 1)

def test_dry_run_creates_and_records_nothing(tmp_path):
    db = tmp_path / "intel.db"; _make_tables(str(db))
    cands = [_cand("m1", "Recruiter")]
    reply_calls, summary_calls = [], []
    res = auto.run_auto_triage(
        cands, lambda c: {"classification": "draft", "draft_body": "Hi"},
        lambda *a: reply_calls.append(a) or "d", lambda *a: summary_calls.append(a) or "s",
        self_email="paul@x.com", db_path=str(db), today="2026-05-30", dry_run=True)
    assert res["drafted"] == 1            # reports the plan
    assert reply_calls == [] and summary_calls == []  # but did nothing
    conn = sqlite3.connect(str(db))
    assert conn.execute("SELECT COUNT(*) FROM triage_actions").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM triage_runs").fetchone()[0] == 0
    conn.close()

def test_no_candidates_records_zero_run_no_summary(tmp_path):
    db = tmp_path / "intel.db"; _make_tables(str(db))
    summary_calls = []
    res = auto.run_auto_triage([], lambda c: {}, lambda *a: "d",
                               lambda *a: summary_calls.append(a) or "s",
                               self_email="paul@x.com", db_path=str(db),
                               log_path=str(tmp_path / "log.md"), today="2026-05-30")
    assert res["seen"] == 0 and res["summary_draft_id"] is None
    assert summary_calls == []
    conn = sqlite3.connect(str(db))
    assert conn.execute("SELECT seen FROM triage_runs").fetchone()[0] == 0  # cadence still logged
    conn.close()

def test_all_ignored_records_run_but_no_summary(tmp_path):
    db = tmp_path / "intel.db"; _make_tables(str(db))
    summary_calls = []
    res = auto.run_auto_triage(
        [_cand("m1", "Newsletter"), _cand("m2", "Promo")],
        lambda c: {"classification": "ignore", "draft_body": ""},
        lambda *a: "d", lambda *a: summary_calls.append(a) or "s",
        self_email="paul@x.com", db_path=str(db), log_path=str(tmp_path / "log.md"), today="2026-05-30")
    assert res["ignored"] == 2 and res["summary_draft_id"] is None
    assert summary_calls == []  # nothing needs Paul, so no summary clutter
    conn = sqlite3.connect(str(db))
    assert conn.execute("SELECT seen FROM triage_runs").fetchone()[0] == 2  # run still logged
    conn.close()


def test_gray_zone_is_never_drafted(tmp_path):
    db = tmp_path / "intel.db"; _make_tables(str(db))
    reply_calls = []
    auto.run_auto_triage([_cand("m1", "Salary negotiation")],
                         lambda c: {"classification": "gray-zone", "draft_body": "should not be used"},
                         lambda *a: reply_calls.append(a) or "d", lambda *a: "s",
                         self_email="paul@x.com", db_path=str(db),
                         log_path=str(tmp_path / "log.md"), today="2026-05-30")
    assert reply_calls == []  # safety invariant: gray-zone never creates a reply draft
