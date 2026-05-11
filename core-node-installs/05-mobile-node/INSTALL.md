# Mobile Node — Install Guide
<!-- v1.0.0 -->

> Layer: F (Flow)
> Installs a Telegram bot for full AIOS access from your phone.

---

## What This Node Does

Creates a Telegram bot connected to your workspace. You can ask questions, query metrics, and receive the Coffee Debrief — all from your phone. Secure: only whitelisted chat IDs can interact with the bot.

---

## Setup Questions

Ask these before doing anything. Each answer configures how the bot behaves.

1. **Have you used Telegram before, and do you already have a bot set up?**
   *(Yes to both = just need the token. No = walk through downloading Telegram and BotFather step by step.)*

2. **What would you primarily use the bot for — quick data queries, asking business questions, capturing ideas, or all of the above?**
   *(Helps set the right persona and frame the bot correctly for how they'll actually use it)*

3. **What communication style do you want from your AI assistant on your phone?**
   *Executive: short, direct, no filler — built for when you're between meetings.*
   *Analyst: more detail, includes numbers and reasoning — built for when you have a few minutes.*
   *Assistant: balanced, clear, conversational — good general default.*
   *(Sets BOT_PERSONA in .env)*

4. **Do you want to be able to send voice notes to the bot and have it respond?**
   *(Yes = set up Whisper transcription, needs OpenAI API key. No = skip voice entirely — text only.)*

5. **Who else, if anyone, should have access to the bot? Or just you?**
   *(Just me = single chat ID in allowlist. Team = collect multiple IDs. Sets TELEGRAM_CHAT_ID_ALLOWLIST.)*

Use these answers to configure BOT_PERSONA, the allowlist, and whether to include voice setup. Skip the Whisper steps entirely if they said no to voice.

---

## Prerequisites

- [ ] Vault Node and Context Node installed
- [ ] Python 3.10+ with venv active and requirements.txt installed
- [ ] Telegram account
- [ ] Anthropic API key (Claude Haiku powers bot responses)

---

## .env Variables Required

| Variable | Description | Where to get it |
|----------|-------------|----------------|
| `TELEGRAM_BOT_TOKEN` | Your bot's token | @BotFather on Telegram |
| `TELEGRAM_CHAT_ID` | Your chat ID | @userinfobot on Telegram |
| `TELEGRAM_CHAT_ID_ALLOWLIST` | Comma-separated allowed chat IDs | Same as TELEGRAM_CHAT_ID for solo use |
| `ANTHROPIC_API_KEY` | Claude API for bot responses | console.anthropic.com |
| `OPENAI_API_KEY` | Whisper for voice notes (optional) | platform.openai.com |
| `BOT_PERSONA` | `executive`, `analyst`, or `assistant` | Set in .env |

---

## Files Installed

| File | What it does |
|------|-------------|
| `flow/bot/main.py` | Bot entry point — handles messages, registers handlers |
| `flow/bot/worker.py` | Core agent — loads context, calls Claude, returns response |
| `flow/bot/voice.py` | Voice note handler — Whisper transcription |
| `flow/bot/config.py` | Reads .env vars, defines allowed chat IDs |

---

## Setup Steps

1. **Create your Telegram bot:**
   - Open Telegram, message `@BotFather`
   - Send: `/newbot`
   - Enter a name (e.g., "My AIOS")
   - Enter a username (must end in `bot`, e.g., `my_aios_bot`)
   - BotFather returns a token — copy it

2. **Get your chat ID:**
   - Message `@userinfobot` on Telegram
   - It replies with your chat ID — copy it

3. **Add to `.env`:**
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   TELEGRAM_CHAT_ID_ALLOWLIST=your_chat_id_here
   ANTHROPIC_API_KEY=your_anthropic_key
   ```

4. **Test the bot locally:**
   ```bash
   python flow/bot/main.py
   ```
   Send a message to your bot in Telegram. It should respond within 10 seconds.

5. **Test a metrics query:**
   Send: "What's my YouTube subscriber count?"
   Should return data from `reach/metrics.md`.

6. **Test voice notes** (optional):
   - Record a voice note in Telegram and send it to the bot
   - Should transcribe and respond

7. **Run the bot in the background:**

   **Windows:**
   Create `flow/bot/start_bot.bat`:
   ```bat
   @echo off
   cd /d "%~dp0..\.."
   .venv\Scripts\pythonw flow\bot\main.py
   ```
   Run this bat file to start the bot without a terminal window.

   Or use Windows Task Scheduler to run on login.

   **Mac/Linux:**
   ```bash
   nohup python flow/bot/main.py &
   ```
   Or use a systemd service for production.

---

## Security

The bot will refuse messages from any chat ID not in `TELEGRAM_CHAT_ID_ALLOWLIST`. Test this:
- Have a friend message your bot → it should reply "Access denied."
- Only your chat ID should work.

Never share your bot token. If compromised, revoke it immediately via @BotFather (`/revoke`).

---

## Validation

1. Send "Hello" to your bot → receives a response
2. Send "What's my current strategy?" → bot summarizes from CRAFT.md
3. Send from an unregistered account → receives "Access denied."
4. Send a voice note → transcribed and answered correctly

---

## Next Steps

Install the Coffee Debrief Node to receive your morning brief in Telegram:
```
/install core-node-installs/04-coffee-debrief-node
```

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | Initial release | Stateless query agent + Whisper voice |
