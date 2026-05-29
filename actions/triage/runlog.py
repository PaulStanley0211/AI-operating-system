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
