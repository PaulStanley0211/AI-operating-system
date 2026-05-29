# gmail.py — v1.0.0
# Gmail inbox collector via OAuth2 REST API.
# Pulls last 7 days of inbox, noise-filtered, stores in intel.db.
# Run reach/auth/gmail_auth.py once before using this collector.

import sys
import json
import base64
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import GMAIL_CREDENTIALS_PATH, GMAIL_TOKEN_PATH, INTEL_DB_PATH
from db import get_conn

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Labels/senders to treat as noise and skip
NOISE_PATTERNS = [
    "noreply@", "no-reply@", "donotreply@",
    "notifications@", "mailer@", "bounce@",
]

NOISE_SUBJECTS = [
    "unsubscribe", "newsletter", "digest", "weekly roundup",
    "your receipt", "invoice #", "order confirmation",
]


def is_noise(sender: str, subject: str) -> bool:
    sender_l = sender.lower()
    subject_l = subject.lower()
    return (
        any(p in sender_l for p in NOISE_PATTERNS)
        or any(p in subject_l for p in NOISE_SUBJECTS)
    )


def get_body_preview(payload: dict, max_chars: int = 500) -> str:
    """Extract plain text preview from a Gmail message payload."""
    def decode_part(part):
        data = part.get("body", {}).get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
        return ""

    mime_type = payload.get("mimeType", "")
    if mime_type == "text/plain":
        return decode_part(payload)[:max_chars]

    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            text = decode_part(part)
            if text:
                return text[:max_chars]

    return ""


def collect(days_back: int = 7):
    creds_path = Path(GMAIL_CREDENTIALS_PATH)
    token_path = Path(GMAIL_TOKEN_PATH)

    if not token_path.exists():
        print("Gmail: no token found — run reach/auth/gmail_auth.py first")
        return

    creds = Credentials.from_authorized_user_file(str(token_path))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    after_ts = int((datetime.now() - timedelta(days=days_back)).timestamp())
    query = f"in:inbox after:{after_ts}"

    results = service.users().messages().list(
        userId="me", q=query, maxResults=100
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        print("Gmail: no recent messages found")
        return

    conn = get_conn(INTEL_DB_PATH)
    c = conn.cursor()
    saved = 0

    for msg_ref in messages:
        msg = service.users().messages().get(
            userId="me", id=msg_ref["id"], format="full"
        ).execute()

        headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}
        sender = headers.get("From", "")
        subject = headers.get("Subject", "(no subject)")
        date_str = headers.get("Date", "")
        message_id = headers.get("Message-ID", msg_ref["id"])

        if is_noise(sender, subject):
            continue

        thread_id = msg.get("threadId", "")
        body_preview = get_body_preview(msg["payload"])
        labels = ",".join(msg.get("labelIds", []))

        try:
            c.execute("""
                INSERT OR IGNORE INTO emails
                (source, message_id, thread_id, date, sender, subject, body_preview, labels)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, ("gmail", message_id, thread_id, date_str, sender, subject, body_preview, labels))
            saved += 1
        except Exception:
            pass

    conn.commit()
    conn.close()
    print(f"Gmail: {saved} emails saved (from {len(messages)} fetched, noise filtered)")


if __name__ == "__main__":
    collect()
