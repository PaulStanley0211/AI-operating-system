# outlook_auth.py — v1.0.0
# One-time device code authorization for Outlook/Microsoft 365.
# Run this once: python reach/auth/outlook_auth.py
# Follow the printed URL + code, sign in, done. Token is cached.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "collectors"))
from config import OUTLOOK_CLIENT_ID, OUTLOOK_TENANT_ID

import msal

TOKEN_CACHE_PATH = Path(__file__).parent / "msal_token_cache.json"
SCOPES = ["Mail.Read"]


def main():
    if not OUTLOOK_CLIENT_ID:
        print("ERROR: OUTLOOK_CLIENT_ID not set in .env")
        print("Register an app at portal.azure.com → Azure Active Directory → App registrations")
        return

    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE_PATH.exists():
        cache.deserialize(TOKEN_CACHE_PATH.read_text())

    app = msal.PublicClientApplication(
        OUTLOOK_CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{OUTLOOK_TENANT_ID or 'common'}",
        token_cache=cache,
    )

    # Check for existing valid token
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            print("✅ Outlook already authorized (token still valid)")
            return

    # Device code flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        print(f"ERROR: Failed to create device flow: {flow.get('error_description')}")
        return

    print(f"\n{flow['message']}\n")
    print("Waiting for authorization...")

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        if cache.has_state_changed:
            TOKEN_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            TOKEN_CACHE_PATH.write_text(cache.serialize())
        print("✅ Outlook authorized. Token cached.")
        print("You can now run: python reach/collectors/outlook.py")
    else:
        print(f"ERROR: {result.get('error_description', 'Authorization failed')}")


if __name__ == "__main__":
    main()
