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

def test_record_run_credits_drafts_plus_triage_scan(tmp_path):
    db = tmp_path / "intel.db"; _make_runs_table(str(db))
    log = tmp_path / "log.md"
    est = runlog.record_run(seen=10, drafted=3, surfaced=1, ignored=6,
                            run_date="2026-05-29", db_path=str(db), log_path=str(log))
    expected = 3 * runlog.MINUTES_PER_DRAFT + runlog.TRIAGE_MINUTES_PER_RUN
    assert est == expected
    conn = sqlite3.connect(str(db))
    row = conn.execute("SELECT seen, drafted, est_minutes_saved FROM triage_runs").fetchone()
    conn.close()
    assert row == (10, 3, expected)
    assert log.exists() and "2026-05-29" in log.read_text()

def test_record_run_no_credit_when_nothing_seen(tmp_path):
    db = tmp_path / "intel.db"; _make_runs_table(str(db))
    est = runlog.record_run(seen=0, drafted=0, surfaced=0, ignored=0,
                            run_date="2026-05-29", db_path=str(db), log_path=str(tmp_path/"l.md"))
    assert est == 0

def test_record_run_triage_credit_without_drafts(tmp_path):
    db = tmp_path / "intel.db"; _make_runs_table(str(db))
    est = runlog.record_run(seen=8, drafted=0, surfaced=1, ignored=7,
                            run_date="2026-05-29", db_path=str(db), log_path=str(tmp_path/"l.md"))
    assert est == runlog.TRIAGE_MINUTES_PER_RUN

def test_weekly_rollup_breakdown(tmp_path):
    db = tmp_path / "intel.db"; _make_runs_table(str(db))
    today = datetime.date(2026, 5, 29)
    # in-window (today and 6 days ago) and out-of-window (7 days ago)
    runlog.record_run(5, 2, 0, 3, run_date="2026-05-29", db_path=str(db), log_path=str(tmp_path/"l.md"))
    runlog.record_run(5, 1, 0, 4, run_date="2026-05-23", db_path=str(db), log_path=str(tmp_path/"l.md"))
    runlog.record_run(5, 9, 0, 0, run_date="2026-05-22", db_path=str(db), log_path=str(tmp_path/"l.md"))
    r = runlog.weekly_rollup(db_path=str(db), today=today)
    assert r["drafts"] == 3                                       # 2 + 1, excludes the 22nd
    assert r["draft_minutes"] == 3 * runlog.MINUTES_PER_DRAFT
    assert r["scans"] == 2                                        # both in-window runs saw email
    assert r["triage_minutes"] == 2 * runlog.TRIAGE_MINUTES_PER_RUN
    assert r["total_minutes"] == r["draft_minutes"] + r["triage_minutes"]
    assert r["noise_filtered"] == 7                              # 3 + 4
    assert r["runs"] == 2

def test_weekly_rollup_excludes_triage_credit_for_empty_runs(tmp_path):
    db = tmp_path / "intel.db"; _make_runs_table(str(db))
    today = datetime.date(2026, 5, 29)
    runlog.record_run(0, 0, 0, 0, run_date="2026-05-28", db_path=str(db), log_path=str(tmp_path/"l.md"))
    runlog.record_run(4, 1, 0, 3, run_date="2026-05-29", db_path=str(db), log_path=str(tmp_path/"l.md"))
    r = runlog.weekly_rollup(db_path=str(db), today=today)
    assert r["runs"] == 2                  # both runs counted
    assert r["scans"] == 1                 # only the run that saw email earns triage credit
    assert r["triage_minutes"] == runlog.TRIAGE_MINUTES_PER_RUN
    assert r["drafts"] == 1
