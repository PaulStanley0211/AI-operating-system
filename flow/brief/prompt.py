# prompt.py — v1.0.0
# Assembles the mega-prompt for the Coffee Debrief from all data sources.
# Returns a tuple: (system_prompt, user_prompt)

import sqlite3
import json
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
CRAFT_MD = ROOT / "CRAFT.md"
METRICS_MD = ROOT / "reach" / "metrics.md"
INTEL_DB = ROOT / "reach" / "data" / "intel.db"

FOUNDER_PRESET = """You are generating a daily intelligence brief for a business owner.

Format the brief with these sections:
1. Executive Summary (2–3 sentences: most important thing, one decision needed)
2. Key Signals (3–5 bullets from data)
3. Metrics Snapshot (table of key numbers)
4. Email Digest (classified inbox summary)
5. Yesterday's Meetings (if any)
6. Recommendations (2–3 specific next actions, ranked by urgency)

Keep it tight. The reader has coffee and 5 minutes. No filler."""

OPERATOR_PRESET = """You are generating a detailed daily operational brief for a business operator.

Format the brief with these sections:
1. Executive Summary
2. Key Signals (5–8 bullets)
3. Metrics vs. Yesterday and 7-day average
4. Email Digest with full classification breakdown
5. Meeting Summaries and Action Items
6. Pipeline / Project Updates
7. Recommendations (3–5 actions)
8. Action Items for Today

Be thorough. The reader will use this to run the business for the day."""


def load_craft_context(max_chars: int = 2000) -> str:
    if not CRAFT_MD.exists():
        return ""
    text = CRAFT_MD.read_text(encoding="utf-8")
    return text[:max_chars]


def load_metrics() -> str:
    if not METRICS_MD.exists():
        return "No metrics available."
    return METRICS_MD.read_text(encoding="utf-8")


def load_emails(days_back: int = 1) -> str:
    if not INTEL_DB.exists():
        return "No email data available."

    conn = sqlite3.connect(str(INTEL_DB))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    cutoff = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    c.execute("""
        SELECT source, date, sender, subject, body_preview
        FROM emails
        WHERE date >= ?
        ORDER BY date DESC
        LIMIT 30
    """, (cutoff,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "No emails in the last 24 hours."

    lines = [f"## Emails (last {days_back} day{'s' if days_back > 1 else ''})"]
    for r in rows:
        lines.append(f"\n**From:** {r['sender']}")
        lines.append(f"**Subject:** {r['subject']}")
        lines.append(f"**Preview:** {r['body_preview'][:200]}")
    return "\n".join(lines)


def load_meetings(count: int = 3) -> str:
    if not INTEL_DB.exists():
        return "No meeting data available."

    conn = sqlite3.connect(str(INTEL_DB))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
        SELECT title, date, duration_minutes, participants, summary, action_items
        FROM meetings
        ORDER BY date DESC
        LIMIT ?
    """, (count,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "No recent meetings."

    lines = [f"## Recent Meetings (last {count})"]
    for r in rows:
        participants = json.loads(r["participants"] or "[]")
        action_items = json.loads(r["action_items"] or "[]")
        lines.append(f"\n**{r['title']}** — {r['date']} ({r['duration_minutes']} min)")
        if participants:
            lines.append(f"Participants: {', '.join(participants)}")
        if r["summary"]:
            lines.append(f"Summary: {r['summary'][:500]}")
        if action_items:
            lines.append(f"Action items: {'; '.join(str(a) for a in action_items[:5])}")
    return "\n".join(lines)


def build_prompt(preset: str = "founder") -> tuple[str, str]:
    system_prompt = FOUNDER_PRESET if preset == "founder" else OPERATOR_PRESET

    today = datetime.now().strftime("%A, %B %d, %Y")
    craft_context = load_craft_context()
    metrics = load_metrics()
    emails = load_emails(days_back=1)
    meetings = load_meetings(count=3)

    user_prompt = f"""Date: {today}

--- BUSINESS CONTEXT ---
{craft_context}

--- CURRENT METRICS ---
{metrics}

--- EMAIL INBOX ---
{emails}

--- RECENT MEETINGS ---
{meetings}

Generate the daily brief now."""

    return system_prompt, user_prompt


if __name__ == "__main__":
    sys_p, usr_p = build_prompt()
    print("=== SYSTEM PROMPT ===")
    print(sys_p)
    print("\n=== USER PROMPT ===")
    print(usr_p[:2000], "...")
    print(f"\nTotal user prompt length: {len(usr_p)} chars")
