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
