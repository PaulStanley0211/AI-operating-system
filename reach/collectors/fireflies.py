# fireflies.py — v1.0.0
# Fireflies.ai meeting transcript collector via GraphQL API.
# Pulls last 30 days of meetings on first run, then daily incremental.

import sys
import json
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import FIREFLIES_API_KEY, INTEL_DB_PATH
from db import get_conn

import requests

GRAPHQL_URL = "https://api.fireflies.ai/graphql"


def query_transcripts(from_date: str) -> list:
    query = """
    query Transcripts($fromDate: String) {
        transcripts(fromDate: $fromDate) {
            id
            title
            date
            duration
            participants
            summary {
                overview
                action_items
            }
        }
    }
    """
    headers = {
        "Authorization": f"Bearer {FIREFLIES_API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": {"fromDate": from_date}},
        headers=headers,
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"Fireflies: API error {resp.status_code}")
        return []
    data = resp.json()
    return data.get("data", {}).get("transcripts", []) or []


def collect(days_back: int = 30):
    if not FIREFLIES_API_KEY:
        print("Fireflies: skipping — FIREFLIES_API_KEY not set")
        return

    conn = get_conn(INTEL_DB_PATH)
    c = conn.cursor()

    # Determine how far back to look — incremental after first run
    c.execute("SELECT MAX(date) FROM meetings WHERE source_id LIKE 'ff_%'")
    row = c.fetchone()
    if row and row[0]:
        days_back = 2  # incremental: just last 2 days
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    transcripts = query_transcripts(from_date)
    saved = 0

    for t in transcripts:
        participants = json.dumps(t.get("participants", []))
        summary_data = t.get("summary") or {}
        summary = summary_data.get("overview", "")
        action_items = json.dumps(summary_data.get("action_items", []))
        duration = t.get("duration", 0)
        if duration:
            duration = int(duration / 60)  # convert seconds to minutes

        try:
            c.execute("""
                INSERT OR IGNORE INTO meetings
                (source_id, title, date, duration_minutes, participants, summary, action_items)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"ff_{t['id']}",
                t.get("title", "Untitled Meeting"),
                t.get("date", ""),
                duration,
                participants,
                summary,
                action_items,
            ))
            saved += 1
        except Exception:
            pass

    conn.commit()
    conn.close()
    print(f"Fireflies: {saved} meetings saved (from {len(transcripts)} fetched)")


if __name__ == "__main__":
    collect()
