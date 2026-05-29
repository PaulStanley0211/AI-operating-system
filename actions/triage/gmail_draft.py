"""Builds threaded plain-text reply MIME and creates Gmail drafts.
Requires a token with the gmail.compose scope. Never sends — only creates drafts."""
import base64
from email.message import EmailMessage
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TOKEN_PATH = str(_ROOT / "reach" / "auth" / "token.json")


def build_reply_mime(to, subject, body, in_reply_to=None, references=None):
    msg = EmailMessage()
    msg["To"] = to
    subject = subject or ""
    msg["Subject"] = subject if subject.lower().startswith("re:") else f"Re: {subject}"
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = references or in_reply_to
    msg.set_content(body)
    return msg


def _encode(msg):
    return base64.urlsafe_b64encode(msg.as_bytes()).decode()


def create_reply_draft(service, thread_id, to, subject, body,
                       in_reply_to=None, references=None):
    msg = build_reply_mime(to, subject, body, in_reply_to, references)
    body_obj = {"message": {"raw": _encode(msg), "threadId": thread_id}}
    draft = service.users().drafts().create(userId="me", body=body_obj).execute()
    return draft["id"]


def create_simple_draft(service, to, subject, body):
    """Create a standalone (non-threaded) draft, e.g. a triage summary to self."""
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    draft = service.users().drafts().create(
        userId="me", body={"message": {"raw": _encode(msg)}}).execute()
    return draft["id"]


def get_gmail_service(token_path=DEFAULT_TOKEN_PATH):
    """Build a Gmail API service from the saved token (lazy imports so tests
    that only exercise the pure builders don't need google libs)."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_file(str(token_path))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        Path(token_path).write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)
