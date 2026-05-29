"""Headless daily triage runner. Classifies new inbox candidates and, for
genuine human messages, drafts a reply in Paul's voice into Gmail Drafts.
NEVER sends. NEVER drafts gray-zone/sensitive items (only surfaces them).
Designed to run unattended on a schedule; Paul reviews + sends from Gmail."""
import json
import re
import sqlite3
import datetime
from pathlib import Path

from actions.triage.runlog import record_run, DEFAULT_DB_PATH, DEFAULT_LOG_PATH

_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL = "claude-sonnet-4-6"


def parse_classification(text):
    """Parse the model's JSON verdict. Defaults to gray-zone on any failure
    (the safe choice: surfaces for human review, never auto-drafts)."""
    t = (text or "").strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
        t = re.sub(r"\n?```$", "", t).strip()
    try:
        d = json.loads(t)
        cls = str(d.get("classification", "")).strip().lower()
        if cls not in ("draft", "gray-zone", "ignore"):
            cls = "gray-zone"
        body = d.get("draft_body") or ""
        return {"classification": cls, "draft_body": body if cls == "draft" else ""}
    except Exception:
        return {"classification": "gray-zone", "draft_body": ""}


def build_system_prompt(profile_text, voice_text):
    return f"""You are Paul's inbox triage assistant. Classify ONE email and, only if it is a genuine human message worth a reply, draft that reply in Paul's voice.

Classify into exactly one of:
- "ignore": newsletters, promotions, automated notifications, receipts, no-reply senders, machine noise.
- "gray-zone": negotiations, declines, rejections, salary discussions, or anything sensitive. NEVER draft these; Paul writes them himself.
- "draft": a real human with a genuine purpose (recruiters, hiring managers, interview scheduling, application follow-ups, prospective clients, direct questions).
When unsure between draft and gray-zone, choose gray-zone.

--- EMAIL PROFILE (Paul's rules) ---
{profile_text}

--- VOICE (match this when drafting) ---
{voice_text}

If classification is "draft", write a short reply in Paul's voice: lead with the point, short sentences, warm not formal, obey the banned-words list (no em dashes, no "delve into", "leverage" as a verb, "robust", etc.), sign off "Kind regards, Paul" for recruiters/hiring managers/clients. Only address what the email actually asks.

Respond with a single JSON object and nothing else:
{{"classification": "ignore|gray-zone|draft", "draft_body": "the reply text, or empty string if not a draft"}}"""


def classify_and_draft(client, candidate, system_prompt, model=DEFAULT_MODEL):
    user = (f"From: {candidate.get('sender','')}\n"
            f"Subject: {candidate.get('subject','')}\n\n"
            f"{candidate.get('body_preview','')}")
    msg = client.messages.create(
        model=model, max_tokens=700, system=system_prompt,
        messages=[{"role": "user", "content": user}],
    )
    return parse_classification(msg.content[0].text)


def _build_summary(drafted, surfaced, ignored_count, date):
    lines = [f"Triage ran {date}.", ""]
    lines.append(f"Drafts created ({len(drafted)}) - review and send in Gmail Drafts:")
    for c in drafted:
        lines.append(f"  - {c.get('subject','')} (from {c.get('sender','')})")
    lines.append("")
    lines.append(f"Gray-zone - you handle these yourself ({len(surfaced)}):")
    for c in surfaced:
        lines.append(f"  - {c.get('subject','')} (from {c.get('sender','')})")
    lines.append("")
    lines.append(f"Ignored as noise: {ignored_count}")
    return "\n".join(lines)


def _record_actions(db_path, rows, today):
    conn = sqlite3.connect(db_path)
    for mid, cls, action, did in rows:
        conn.execute(
            "INSERT OR IGNORE INTO triage_actions (message_id, classification, action, draft_id, run_date)"
            " VALUES (?,?,?,?,?)", (mid, cls, action, did, today))
    conn.commit(); conn.close()


def run_auto_triage(candidates, classifier, make_reply_draft, make_summary_draft,
                    self_email, db_path=DEFAULT_DB_PATH, log_path=DEFAULT_LOG_PATH,
                    today=None, dry_run=False):
    """Route each candidate (draft / gray-zone / ignore), create Gmail drafts for
    genuine human messages, surface gray-zone, and write a summary draft. Records
    actions + the run unless dry_run. Returns the run counts."""
    today = today or datetime.date.today().isoformat()
    drafted_items, surfaced_items = [], []
    drafted = surfaced = ignored = 0
    rows = []
    for c in candidates:
        verdict = classifier(c) or {}
        cls = verdict.get("classification", "gray-zone")
        if cls == "draft":
            did = None if dry_run else make_reply_draft(
                c["thread_id"], c["sender"], c["subject"], verdict.get("draft_body", ""), c["message_id"])
            rows.append((c["message_id"], "draft", "drafted", did))
            drafted_items.append(c); drafted += 1
        elif cls == "gray-zone":
            rows.append((c["message_id"], "gray-zone", "surfaced", None))
            surfaced_items.append(c); surfaced += 1
        else:
            rows.append((c["message_id"], "ignore", "ignored", None))
            ignored += 1

    summary_id = None
    if not dry_run:
        if drafted or surfaced:  # only summarize when something needs Paul's attention
            summary_id = make_summary_draft(
                self_email, f"Triage summary {today}",
                _build_summary(drafted_items, surfaced_items, ignored, today))
        _record_actions(db_path, rows, today)
        record_run(seen=len(candidates), drafted=drafted, surfaced=surfaced,
                   ignored=ignored, run_date=today, db_path=db_path, log_path=log_path)

    return {"seen": len(candidates), "drafted": drafted, "surfaced": surfaced,
            "ignored": ignored, "summary_draft_id": summary_id}


def main(dry_run=False):
    import os
    from dotenv import load_dotenv
    import anthropic
    from actions.triage.emails import get_candidates
    from actions.triage.gmail_draft import get_gmail_service, create_reply_draft, create_simple_draft

    load_dotenv(_ROOT / ".env")
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ANTHROPIC_API_KEY missing from .env"); return

    profile = (_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    voice = (_ROOT / "context" / "voice" / "samples.md").read_text(encoding="utf-8")[:4000]
    system_prompt = build_system_prompt(profile, voice)
    client = anthropic.Anthropic(api_key=key)
    model = os.environ.get("TRIAGE_MODEL", DEFAULT_MODEL)

    cands, refreshed = get_candidates(refresh=True)
    svc = get_gmail_service()
    self_email = svc.users().getProfile(userId="me").execute().get("emailAddress")

    def make_reply(thread_id, to, subject, body, in_reply_to):
        return create_reply_draft(svc, thread_id, to, subject, body, in_reply_to)

    def make_summary(to, subject, body):
        return create_simple_draft(svc, to, subject, body)

    res = run_auto_triage(
        cands, lambda c: classify_and_draft(client, c, system_prompt, model),
        make_reply, make_summary, self_email=self_email, dry_run=dry_run)
    print("AUTO-TRIAGE", "DRY-RUN" if dry_run else "LIVE", "refreshed:", refreshed, res)


if __name__ == "__main__":
    import sys
    main(dry_run="--dry-run" in sys.argv)
