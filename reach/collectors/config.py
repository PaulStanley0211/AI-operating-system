# config.py — v1.0.0
# Loads .env and exposes API keys as constants.

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the workspace root (two levels up from this file)
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# YouTube
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "")

# Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")

# Gmail
GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", "reach/auth/gmail_credentials.json")
GMAIL_TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "reach/auth/token.json")

# Outlook
OUTLOOK_CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID", "")
OUTLOOK_TENANT_ID = os.getenv("OUTLOOK_TENANT_ID", "")

# Fireflies
FIREFLIES_API_KEY = os.getenv("FIREFLIES_API_KEY", "")

# FX Rates
OPEN_EXCHANGE_RATES_APP_ID = os.getenv("OPEN_EXCHANGE_RATES_APP_ID", "")

# Database paths
DB_PATH = str(Path(__file__).parent.parent / "data" / "data.db")
INTEL_DB_PATH = str(Path(__file__).parent.parent / "data" / "intel.db")
