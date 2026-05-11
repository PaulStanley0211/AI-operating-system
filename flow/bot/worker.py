# worker.py — v1.0.0
# Core agent: loads context, calls Claude, returns response.
# Each message is handled independently (stateless).

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import ANTHROPIC_API_KEY, BOT_PERSONA, CRAFT_MD, METRICS_MD

import anthropic

PERSONA_NOTES = {
    "executive": "Keep responses short and punchy — under 150 words. High-level, decisive.",
    "analyst": "Be thorough. Include numbers and reasoning. Up to 400 words if needed.",
    "assistant": "Balanced — clear and helpful. Under 250 words. Plain text only (no markdown).",
}


def build_system_prompt() -> str:
    craft_context = ""
    if CRAFT_MD.exists():
        craft_context = CRAFT_MD.read_text(encoding="utf-8")[:3000]

    metrics_context = ""
    if METRICS_MD.exists():
        metrics_context = METRICS_MD.read_text(encoding="utf-8")[:2000]

    persona_note = PERSONA_NOTES.get(BOT_PERSONA, PERSONA_NOTES["assistant"])

    return f"""You are a mobile AI assistant for a business owner. You have access to their business context and current metrics.

{persona_note}

This is a Telegram bot — plain text only. No markdown formatting, no bullet points with *, no headers with #. Use line breaks for structure.

--- BUSINESS CONTEXT ---
{craft_context}

--- CURRENT METRICS ---
{metrics_context if metrics_context else "No metrics data available. The Intelligence Node may not be installed yet."}
"""


def respond(user_message: str) -> str:
    if not ANTHROPIC_API_KEY:
        return "Bot not configured — ANTHROPIC_API_KEY is missing from .env"

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=build_system_prompt(),
        messages=[{"role": "user", "content": user_message}],
    )

    return message.content[0].text
