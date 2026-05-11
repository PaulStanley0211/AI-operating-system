# deliver.py — v1.0.0
# Delivers the daily brief and chart to Telegram.

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
CHART_PATH = Path(__file__).parent / "dashboard.png"

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_text(text: str) -> bool:
    if not BOT_TOKEN or not CHAT_ID:
        print("Deliver: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set — printing to console")
        print(text)
        return False

    # Telegram has a 4096 char limit per message — split if needed
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    for chunk in chunks:
        resp = requests.post(f"{TELEGRAM_API}/sendMessage", json={
            "chat_id": CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown",
        })
        if not resp.ok:
            print(f"Deliver: Telegram text error — {resp.status_code}: {resp.text[:200]}")
            return False
    return True


def send_photo(image_path: str, caption: str = "") -> bool:
    if not BOT_TOKEN or not CHAT_ID:
        return False
    if not Path(image_path).exists():
        print(f"Deliver: image not found at {image_path}")
        return False

    with open(image_path, "rb") as f:
        resp = requests.post(f"{TELEGRAM_API}/sendPhoto", data={
            "chat_id": CHAT_ID,
            "caption": caption[:1000],
        }, files={"photo": f})

    if not resp.ok:
        print(f"Deliver: Telegram photo error — {resp.status_code}: {resp.text[:200]}")
        return False
    return True


def deliver(brief_text: str, chart_path: str = None) -> bool:
    print("Delivering brief to Telegram...")

    # Send chart first if it exists
    if chart_path and Path(chart_path).exists():
        send_photo(chart_path, caption="📊 Daily Metrics")

    # Send the brief text
    success = send_text(brief_text)
    if success:
        print("✅ Brief delivered to Telegram")
    return success


if __name__ == "__main__":
    test_brief = "🔔 *Daily Brief Test*\n\nThis is a test delivery. If you're reading this, the Coffee Debrief Node is working."
    deliver(test_brief, str(CHART_PATH) if CHART_PATH.exists() else None)
