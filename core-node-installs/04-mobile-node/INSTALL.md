# Mobile Node — Install Guide
<!-- v2.0.0 -->

> Layer: F (Flow)
> Installs CommandOS — a Telegram group with persistent AI agents accessible from your phone.

---

## What This Node Does

Creates a Telegram GROUP with forum topics enabled, then installs CommandOS — an AI command interface that runs in that group. Each conversation becomes its own named topic thread. You can ask questions, query metrics, send voice notes, and spawn fresh agents on demand — all from your phone.

This is not a simple chatbot. Each agent session persists context across multiple messages using the Prime → Task pattern: context is loaded once per session, then reused efficiently for every follow-up message.

After this node you have:
- A Telegram group acting as your AIOS command center
- A persistently running bot with topic-based threading
- Voice note support (optional)
- The Telegram credentials needed for the Coffee Debrief Node

---

## Scoping Questions

Ask these before doing anything. Answers determine which dependencies get installed and which deployment path to follow.

1. **Do you want to send voice notes to the bot and have it respond?**
   *(Yes = install OpenAI Whisper, needs OpenAI API key. No = text only, skip voice setup entirely.)*

2. **Do you want the bot to generate formatted PDF reports?**
   *(Yes = install WeasyPrint. No = skip.)*

3. **Do you want the bot to generate charts and graphs?**
   *(Yes = install matplotlib. No = skip.)*

4. **Where will this run — Mac, Linux, or laptop?**
   *(Mac = set up launchd for always-on. Linux = set up systemd. Laptop = run manually when needed.)*

Use these answers to install only what's needed and follow the right deployment path.

---

## Prerequisites

- [ ] Vault Node and Context Node installed
- [ ] Python 3.10+ with venv active and requirements.txt installed
- [ ] Telegram account
- [ ] Anthropic API key

---

## .env Variables Required

| Variable | Required | Description | Where to get it |
|----------|----------|-------------|----------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Your bot's token | @BotFather on Telegram |
| `TELEGRAM_GROUP_ID` | Yes | Your group ID | Extracted via curl after setup (negative number) |
| `ANTHROPIC_API_KEY` | Yes | Claude API for agent sessions | console.anthropic.com — format: `sk-ant-` |
| `OPENAI_API_KEY` | If voice enabled | Whisper for voice transcription | platform.openai.com |
| `VOICE_ENABLED` | If voice enabled | Set to `true` | Set in .env |

---

## Files Installed

| File | What it does |
|------|-------------|
| `flow/bot/main.py` | Entry point — starts aiogram polling loop, shows boot banner |
| `flow/bot/bot.py` | Message handlers, 1.5s debounce, topic routing |
| `flow/bot/orchestrator.py` | Command dispatch (/new, /name, /compact, /reset, /help), delivery |
| `flow/bot/worker.py` | Agent SDK wrapper, system prompt, Prime → Task session pattern |
| `flow/bot/agent_sdk.py` | Claude Agent SDK integration — Prime + Task calls |
| `flow/bot/config.py` | Reads .env: bot token, group ID, feature flags |
| `flow/bot/session_manager.py` | Maps topic thread ID → Agent SDK session ID |
| `flow/bot/formatting.py` | Message splitting, Telegram markdown, image/file delivery |

---

## Setup Steps

### Step 1 — Create the bot

1. Open Telegram → search `@BotFather` (blue checkmark, official)
2. Send: `/newbot`
3. Enter a display name — e.g. "Command Center"
4. Enter a username — must end in `bot`, e.g. `mycommand_bot`
5. BotFather replies with a token: `7123456789:AAHx_your_long_token_here`
6. Copy the full token → add to `.env` as `TELEGRAM_BOT_TOKEN`

### Step 2 — Create the group

1. Create a new Telegram group — name it something like "Command Center"
2. Add your bot to the group
3. Tap the group name → Edit → grant the bot **all administrator permissions**
4. Tap the group name → Edit → toggle **Topics** ON (this is required — it enables the thread-per-conversation model)
5. Send a test message in the group: "hello"

### Step 3 — Get the Group ID

The Group ID is a negative number starting with `-100`.

1. Run this command (replace `YOUR_TOKEN` with your bot token):
   ```bash
   curl "https://api.telegram.org/botYOUR_TOKEN/getUpdates"
   ```
2. In the response, find `"chat":{"id":` — copy the value (e.g. `-1001234567890`)
3. If the response is empty, send another message in the group and retry
4. Add to `.env` as `TELEGRAM_GROUP_ID`

### Step 4 — Get your Anthropic API key

1. Go to console.anthropic.com
2. Click **API Keys** in the left sidebar
3. Click **Create Key** — give it any name
4. Copy the key (starts with `sk-ant-`) → add to `.env` as `ANTHROPIC_API_KEY`

### Step 5 — Get OpenAI key (if voice enabled)

1. Go to platform.openai.com
2. Click your account icon → **API keys**
3. Click **Create new secret key**
4. Copy the key (starts with `sk-`) → add to `.env` as `OPENAI_API_KEY`
5. Also set `VOICE_ENABLED=true` in `.env`

### Step 6 — Install dependencies

```bash
# Core
pip install aiogram claude-agent-sdk python-dotenv markdown

# Optional — install only what scoping said yes to
pip install openai          # voice transcription
pip install weasyprint      # PDF reports
pip install matplotlib      # charts
```

### Step 7 — Test the bot locally

```bash
python -m flow.bot.main
```

When you see "Online — polling" in the terminal, the bot is live. Send a message in your Telegram group — it should respond in a topic thread within 10 seconds.

### Step 8 — Deploy for always-on operation

**Mac (launchd):**
1. Copy `flow/bot/config/com.commandos.bot.plist` to `~/Library/LaunchAgents/`
2. Open the file and replace:
   - `__VENV_PYTHON__` → absolute path to `.venv/bin/python`
   - `__WORKSPACE_ROOT__` → absolute path to your workspace folder
   - `__USERNAME__` → your macOS username
3. Load: `launchctl load ~/Library/LaunchAgents/com.commandos.bot.plist`
4. Verify: `launchctl list | grep commandos`

**Linux (systemd):**
1. Copy `flow/bot/config/command-bot.service` to `/etc/systemd/system/`
2. Replace the same `__VENV_PYTHON__`, `__WORKSPACE_ROOT__`, `__USERNAME__` placeholders
3. Enable + start:
   ```bash
   sudo systemctl enable command-bot
   sudo systemctl start command-bot
   ```
4. Verify: `sudo systemctl status command-bot`

**Laptop (run manually):**
Run `python -m flow.bot.main` when you need it. Close the terminal to stop.

---

## Commands Available Once Deployed

| Command | What it does |
|---------|-------------|
| `/new` | Spawn a fresh Sonnet agent in a new topic thread |
| `/new opus` | Spawn an Opus agent (more capable) |
| `/name` | Auto-rename the current topic based on the conversation |
| `/compact` | Compress context when the agent starts losing track |
| `/reset` | Clear the current session and start fresh |
| `/help` | Show the full command list |
| `/reboot` | Restart the bot process |

---

## Validation

1. Send a message in the group → response appears in a topic thread within 10 seconds
2. Run `/new` → a new topic is created and the agent confirms it has been primed
3. Send a message from outside the group → silently rejected
4. Send a voice note → transcribed and answered (if voice enabled)
5. Run `/name` → topic renames itself based on the conversation content

---

## Next Steps

Install the Coffee Debrief Node to receive your morning brief in this same Telegram group:
```
/install core-node-installs/05-coffee-debrief-node
```

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 2.0.0 | Rewrite | CommandOS group-chat pattern — aiogram + Agent SDK, forum topics, persistent sessions |
| 1.0.0 | Initial release | Stateless DM bot + Whisper voice |
