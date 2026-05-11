# Mobile Node

> Layer: F (Flow)
> Full AIOS access from your phone via Telegram.

---

## What It Is

The Mobile Node creates a Telegram bot connected to your AIOS workspace. You can ask it questions, query your business metrics, get answers from your AI, and capture tasks — all from your phone. The bot is secured so only you (and whoever you authorize) can interact with it.

If you're getting the Coffee Debrief Node, this must be installed first — it provides the Telegram bot that delivers your morning brief.

---

## What It Does

- Creates a Telegram bot that responds to messages in natural language
- Loads your business context (CRAFT.md + metrics.md) on every request so answers are grounded in your actual data
- Supports three response styles: Executive (short and direct), Analyst (detailed with reasoning), or Assistant (balanced)
- Handles text messages and voice notes (with Whisper transcription if enabled)
- Locks the bot to an allowlist of chat IDs — anyone else gets "Access denied"
- Integrates with GTD: send `/capture [task]` to add items to your inbox from anywhere

---

## How to Install

With Vault and Context nodes already installed, run:
```
/install node-installs/mobile-node
```

Claude will ask you 5 setup questions:
1. Whether you've used Telegram before and if you already have a bot set up
2. What you'll primarily use the bot for (quick queries, business questions, capturing ideas, all of the above)
3. What response style you want (Executive / Analyst / Assistant)
4. Whether you want voice note support (requires OpenAI API key for Whisper)
5. Who else, if anyone, should have access to the bot

Your answers configure the bot persona and the allowlist before any code runs.

---

## How to Know It's Working

After install, start the bot:
```bash
python flow/bot/main.py
```

Then open Telegram and send a message to your bot. It should respond within 10 seconds.

Run these three tests:
1. Send: "Hello" → should get a response (confirms bot is running and auth works)
2. Send: "What's my current business strategy?" → should summarize from your context files
3. Have someone else (or a second account) message the bot → should receive "Access denied"

If all three pass, Mobile Node is working.

To run the bot in the background without a terminal window:
```
flow/bot/start_bot.bat   (Windows)
nohup python flow/bot/main.py &   (Mac/Linux)
```

---

## What to Expect

The bot is stateless — it doesn't remember the previous message in a conversation. Each message is answered independently using your context files and metrics. This keeps it fast and simple, but means it's better suited for single-question queries than multi-turn conversations.

For anything requiring deeper work (writing, planning, analysis), use Claude Code on your desktop. The bot is for quick access when you're away from your desk.

Voice note support adds a meaningful level of convenience — hold record, speak your question, get an answer — but requires an OpenAI API key. If you don't have one, skip it for now and add it later by editing `.env` and setting `OPENAI_API_KEY`.

---

## What You Have to Do Yourself

| Task | Notes |
|------|-------|
| Create a Telegram bot via @BotFather | Free — takes 2 minutes in Telegram |
| Get your chat ID from @userinfobot | Free — takes 30 seconds |
| Add bot token and chat ID to `.env` | Copy-paste into the env file |
| Get an OpenAI API key (optional) | platform.openai.com — only needed for voice notes |
| Decide how to run the bot long-term | Task Scheduler (Windows) or systemd/nohup (Mac/Linux) |

**Security reminder:** Never share your bot token. If it's ever compromised, revoke it immediately via @BotFather using `/revoke`.

---

## Next Step

Once Mobile is running, install the Coffee Debrief to get your morning brief delivered:
```
/install node-installs/coffee-debrief-node
```

Or move to task management:
```
/install node-installs/productivity-node
```
