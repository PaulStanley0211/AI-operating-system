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
