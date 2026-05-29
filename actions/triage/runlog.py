"""Records each triage run and computes the weekly time-saved rollup."""
import sqlite3
import datetime
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = str(_ROOT / "reach" / "data" / "intel.db")
DEFAULT_LOG_PATH = str(_ROOT / "tuning" / "triage" / "log.md")
MINUTES_PER_DRAFT = 6  # tunable estimate of minutes saved per drafted reply
TRIAGE_MINUTES_PER_RUN = 3  # tunable estimate of the inbox scan skipped per run


def record_run(seen, drafted, surfaced, ignored, run_date=None,
               db_path=DEFAULT_DB_PATH, log_path=DEFAULT_LOG_PATH):
    run_date = run_date or datetime.date.today().isoformat()
    est = drafted * MINUTES_PER_DRAFT + (TRIAGE_MINUTES_PER_RUN if seen > 0 else 0)
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
        "SELECT COALESCE(SUM(drafted),0) AS drafts,"
        " COALESCE(SUM(CASE WHEN seen > 0 THEN 1 ELSE 0 END),0) AS scans,"
        " COALESCE(SUM(ignored),0) AS noise,"
        " COUNT(*) AS runs FROM triage_runs WHERE run_date >= ?",
        (since,),
    ).fetchone()
    conn.close()
    draft_minutes = row["drafts"] * MINUTES_PER_DRAFT
    triage_minutes = row["scans"] * TRIAGE_MINUTES_PER_RUN
    return {
        "since": since,
        "drafts": row["drafts"],
        "draft_minutes": draft_minutes,
        "scans": row["scans"],
        "triage_minutes": triage_minutes,
        "total_minutes": draft_minutes + triage_minutes,
        "noise_filtered": row["noise"],
        "runs": row["runs"],
    }


def _append_log(run_date, seen, drafted, surfaced, est, log_path):
    p = Path(log_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("# Triage Log\n\n| Date | Seen | Drafted | Surfaced | Est. min saved |\n"
                     "|------|------|---------|----------|----------------|\n", encoding="utf-8")
    with p.open("a", encoding="utf-8") as f:
        f.write(f"| {run_date} | {seen} | {drafted} | {surfaced} | {est} |\n")
