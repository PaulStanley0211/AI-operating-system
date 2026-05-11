# config.py — v1.0.0
# Bot configuration — reads .env and defines security allowlist.

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID_ALLOWLIST_RAW = os.getenv("TELEGRAM_CHAT_ID_ALLOWLIST", "")

# Parse allowlist — comma-separated chat IDs
ALLOWED_CHAT_IDS: set[int] = set()
for cid in CHAT_ID_ALLOWLIST_RAW.split(","):
    cid = cid.strip()
    if cid.lstrip("-").isdigit():
        ALLOWED_CHAT_IDS.add(int(cid))

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
BOT_PERSONA = os.getenv("BOT_PERSONA", "assistant")

ROOT = Path(__file__).parent.parent.parent
CRAFT_MD = ROOT / "CRAFT.md"
METRICS_MD = ROOT / "reach" / "metrics.md"
