# gmail_auth.py — v1.0.0
# One-time OAuth2 authorization for Gmail.
# Run this once: python reach/auth/gmail_auth.py
# It opens a browser, you authorize, and saves token.json.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "collectors"))
from config import GMAIL_CREDENTIALS_PATH, GMAIL_TOKEN_PATH

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
    creds = None
    token_path = Path(GMAIL_TOKEN_PATH)
    creds_path = Path(GMAIL_CREDENTIALS_PATH)

    if not creds_path.exists():
        print(f"ERROR: Gmail credentials not found at {GMAIL_CREDENTIALS_PATH}")
        print("Download from Google Cloud Console: APIs & Services → Credentials → OAuth 2.0 Client")
        return

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)

        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json())

    print(f"Gmail authorized. Token saved to {GMAIL_TOKEN_PATH}")
    print("You can now run: python reach/collectors/gmail.py")


if __name__ == "__main__":
    main()
