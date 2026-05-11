# db.py — v1.0.0
# Database setup, table creation, and connection helpers.
# Run directly to initialize both databases: python reach/collectors/db.py

import sqlite3
from pathlib import Path
from config import DB_PATH, INTEL_DB_PATH


def get_conn(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_data_db():
    conn = get_conn(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS youtube_daily (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            subscribers INTEGER,
            total_views INTEGER,
            video_count INTEGER,
            views_30d INTEGER,
            collected_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(date)
        );

        CREATE TABLE IF NOT EXISTS youtube_videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            date TEXT NOT NULL,
            title TEXT,
            views INTEGER,
            likes INTEGER,
            comments INTEGER,
            published_at TEXT,
            collected_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(video_id, date)
        );

        CREATE TABLE IF NOT EXISTS stripe_daily (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            mrr_cents INTEGER,
            arr_cents INTEGER,
            active_subscribers INTEGER,
            new_customers INTEGER,
            churned_customers INTEGER,
            collected_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(date)
        );

        CREATE TABLE IF NOT EXISTS fx_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            currency TEXT NOT NULL,
            rate_from_usd REAL,
            collected_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(date, currency)
        );
    """)

    conn.commit()
    conn.close()
    print(f"data.db initialized at {DB_PATH}")


def init_intel_db():
    conn = get_conn(INTEL_DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            message_id TEXT UNIQUE,
            date TEXT,
            sender TEXT,
            subject TEXT,
            body_preview TEXT,
            labels TEXT,
            collected_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT UNIQUE,
            title TEXT,
            date TEXT,
            duration_minutes INTEGER,
            participants TEXT,
            summary TEXT,
            action_items TEXT,
            transcript TEXT,
            collected_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
    print(f"intel.db initialized at {INTEL_DB_PATH}")


if __name__ == "__main__":
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(INTEL_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    init_data_db()
    init_intel_db()
    print("Both databases initialized.")
