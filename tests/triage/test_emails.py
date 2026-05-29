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
