# voice.py — v1.0.0
# Voice note handler: downloads OGG from Telegram, transcribes with Whisper API.

import os
import tempfile
from pathlib import Path

import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


def transcribe(file_id: str) -> str:
    """Download a Telegram voice file and transcribe with Whisper. Returns text."""
    if not OPENAI_API_KEY:
        return "[Voice notes require OPENAI_API_KEY in .env]"

    # Get file path from Telegram
    resp = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
        params={"file_id": file_id},
        timeout=10,
    )
    if not resp.ok:
        return "[Failed to get voice file from Telegram]"

    file_path = resp.json()["result"]["file_path"]
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    # Download the audio file
    audio_resp = requests.get(file_url, timeout=30)
    if not audio_resp.ok:
        return "[Failed to download voice file]"

    # Save to temp file and transcribe
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        tmp.write(audio_resp.content)
        tmp_path = tmp.name

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
            )
        return transcript.strip()
    except Exception as e:
        return f"[Transcription error: {e}]"
    finally:
        Path(tmp_path).unlink(missing_ok=True)
