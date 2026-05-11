# outlook.py — v1.0.0
# Outlook/Microsoft 365 inbox collector via Microsoft Graph API (MSAL device code flow).
# Run reach/auth/outlook_auth.py once before using this collector.

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import OUTLOOK_CLIENT_ID, OUTLOOK_TENANT_ID, INTEL_DB_PATH
from db import get_conn

import msal
import requests

GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"
TOKEN_CACHE_PATH = Path(__file__).parent.parent / "auth" / "msal_token_cache.json"
SCOPES = ["Mail.Read"]

NOISE_PATTERNS = [
    "noreply@", "no-reply@", "donotreply@",
    "notifications@", "mailer@",
]
NOISE_SUBJECTS = [
    "unsubscribe", "newsletter", "digest", "your receipt",
    "invoice #", "order confirmation",
]


def is_noise(sender: str, subject: str) -> bool:
    return (
        any(p in sender.lower() for p in NOISE_PATTERNS)
        or any(p in subject.lower() for p in NOISE_SUBJECTS)
    )


def get_token() -> str | None:
    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE_PATH.exists():
        cache.deserialize(TOKEN_CACHE_PATH.read_text())

    app = msal.PublicClientApplication(
        OUTLOOK_CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{OUTLOOK_TENANT_ID}",
        token_cache=cache,
    )

    accounts = app.get_accounts()
    if not accounts:
        print("Outlook: no cached token — run reach/auth/outlook_auth.py first")
        return None

    result = app.acquire_token_silent(SCOPES, account=accounts[0])
    if not result or "access_token" not in result:
        print("Outlook: token refresh failed — run reach/auth/outlook_auth.py again")
        return None

    if cache.has_state_changed:
        TOKEN_CACHE_PATH.write_text(cache.serialize())

    return result["access_token"]


def collect(days_back: int = 7):
    if not OUTLOOK_CLIENT_ID:
        print("Outlook: skipping — OUTLOOK_CLIENT_ID not set")
        return

    token = get_token()
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    cutoff = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%SZ")

    url = (
        f"{GRAPH_ENDPOINT}/me/mailFolders/inbox/messages"
        f"?$filter=receivedDateTime ge {cutoff}"
        f"&$select=id,subject,from,receivedDateTime,bodyPreview"
        f"&$top=100&$orderby=receivedDateTime desc"
    )

    conn = get_conn(INTEL_DB_PATH)
    c = conn.cursor()
    saved = 0

    while url:
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Outlook: API error {resp.status_code}: {resp.text[:200]}")
            break

        data = resp.json()
        for msg in data.get("value", []):
            sender = msg.get("from", {}).get("emailAddress", {}).get("address", "")
            subject = msg.get("subject", "(no subject)")

            if is_noise(sender, subject):
                continue

            try:
                c.execute("""
                    INSERT OR IGNORE INTO emails
                    (source, message_id, date, sender, subject, body_preview, labels)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    "outlook",
                    msg["id"],
                    msg.get("receivedDateTime", ""),
                    sender,
                    subject,
                    msg.get("bodyPreview", "")[:500],
                    "inbox",
                ))
                saved += 1
            except Exception:
                pass

        url = data.get("@odata.nextLink")

    conn.commit()
    conn.close()
    print(f"Outlook: {saved} emails saved")


if __name__ == "__main__":
    collect()
