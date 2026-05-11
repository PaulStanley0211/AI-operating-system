# main.py — v1.0.0
# Telegram bot entry point. Handles messages and voice notes.
# Run: python flow/bot/main.py

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import BOT_TOKEN, ALLOWED_CHAT_IDS

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s — %(levelname)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    # Security: reject unauthorized senders
    if ALLOWED_CHAT_IDS and chat_id not in ALLOWED_CHAT_IDS:
        await update.message.reply_text("Access denied.")
        logger.warning(f"Rejected message from chat_id {chat_id}")
        return

    text = update.message.text or ""

    # /capture command — add to GTD inbox
    if text.startswith("/capture "):
        item = text[9:].strip()
        if item:
            root = Path(__file__).parent.parent.parent
            import subprocess
            result = subprocess.run(
                [sys.executable, str(root / "flow" / "inbox_writer.py"), item],
                capture_output=True, text=True
            )
            await update.message.reply_text(f"Captured to inbox: {item}")
        else:
            await update.message.reply_text("Usage: /capture [item to capture]")
        return

    # Regular message — send to worker
    from worker import respond
    await update.message.reply_chat_action("typing")
    response = respond(text)
    await update.message.reply_text(response)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    if ALLOWED_CHAT_IDS and chat_id not in ALLOWED_CHAT_IDS:
        await update.message.reply_text("Access denied.")
        return

    await update.message.reply_chat_action("typing")

    file_id = update.message.voice.file_id
    from voice import transcribe
    transcript = transcribe(file_id)

    if transcript.startswith("["):
        await update.message.reply_text(transcript)
        return

    # Show the transcription, then respond
    await update.message.reply_text(f"🎤 {transcript}")

    from worker import respond
    response = respond(transcript)
    await update.message.reply_text(response)


def main():
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in .env — cannot start bot")
        sys.exit(1)

    if not ALLOWED_CHAT_IDS:
        logger.warning("TELEGRAM_CHAT_ID_ALLOWLIST is empty — bot will respond to anyone!")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    logger.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
