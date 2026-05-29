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
