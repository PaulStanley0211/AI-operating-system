# collect.py — v1.0.0
# Orchestrator — runs all configured collectors in sequence.
# Run daily via scheduler: python reach/collectors/collect.py

import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from db import init_data_db, init_intel_db
from config import (
    YOUTUBE_API_KEY, STRIPE_SECRET_KEY, FIREFLIES_API_KEY,
    OPEN_EXCHANGE_RATES_APP_ID, GMAIL_TOKEN_PATH, OUTLOOK_CLIENT_ID
)


def run_collector(name, fn):
    try:
        fn()
    except Exception as e:
        print(f"{name}: FAILED — {e}")
        if "--verbose" in sys.argv:
            traceback.print_exc()


def main():
    print("=== CRAFT Data Collection ===")

    # Ensure databases exist
    init_data_db()
    init_intel_db()

    # YouTube
    if YOUTUBE_API_KEY:
        from youtube import collect as collect_youtube
        run_collector("YouTube", collect_youtube)
    else:
        print("YouTube: skipped (no API key)")

    # Stripe
    if STRIPE_SECRET_KEY:
        from stripe_collector import collect as collect_stripe
        run_collector("Stripe", collect_stripe)
    else:
        print("Stripe: skipped (no API key)")

    # FX Rates
    if OPEN_EXCHANGE_RATES_APP_ID:
        from fx_rates import collect as collect_fx
        run_collector("FX Rates", collect_fx)
    else:
        print("FX Rates: skipped (no API key)")

    # Gmail
    if Path(GMAIL_TOKEN_PATH).exists():
        from gmail import collect as collect_gmail
        run_collector("Gmail", collect_gmail)
    else:
        print("Gmail: skipped (run reach/auth/gmail_auth.py to authorize)")

    # Outlook
    if OUTLOOK_CLIENT_ID:
        from outlook import collect as collect_outlook
        run_collector("Outlook", collect_outlook)
    else:
        print("Outlook: skipped (no OUTLOOK_CLIENT_ID)")

    # Fireflies
    if FIREFLIES_API_KEY:
        from fireflies import collect as collect_fireflies
        run_collector("Fireflies", collect_fireflies)
    else:
        print("Fireflies: skipped (no API key)")

    print("=== Collection complete ===")
    print("Run 'python reach/generate_metrics.py' to refresh metrics.md")


if __name__ == "__main__":
    main()
