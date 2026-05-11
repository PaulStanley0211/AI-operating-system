# Coffee Debrief Node — Install Guide
<!-- v1.0.0 -->

> Layer: A (Actions)
> Synthesizes all collected data into a daily morning brief and delivers it to Telegram.

---

## What This Node Does

Assembles your metrics, emails, and meeting transcripts into a structured daily brief. Generates a chart image. Delivers both to your Telegram by 7 AM. By the time you sit down with coffee, you know what happened yesterday and what needs your attention today.

---

## Setup Questions

Ask these before doing anything. Each answer configures how the brief is generated and delivered.

1. **Which AI model do you want generating your daily brief?**
   *Gemini (recommended — ~$0.005/brief, fast, great quality) or Claude (~$0.03/brief, slightly higher quality)*
   *(Sets BRIEF_LLM in .env)*

2. **How much detail do you want in your morning brief?**
   *Founder preset: executive summary, key signals, metrics, email digest — 3–5 min read.*
   *Operator preset: same plus full meeting summaries, pipeline, detailed action items — 8–10 min read.*
   *(Sets BRIEF_PRESET in .env)*

3. **What's the single most important metric in your business right now — the one number that tells you if things are going well?**
   *(Examples: revenue, subscribers, active clients, calls handled. Sets DASHBOARD_METRIC — this is what gets charted.)*

4. **What time do you want the brief delivered each morning?**
   *(Default: 7:00 AM. Sets the scheduler time. Pick something before you usually start work.)*

5. **Is there anything specific you always want the brief to cover — a recurring signal, a person to watch, a project that needs daily visibility?**
   *(Optional — used to customize the brief system prompt so it consistently surfaces what matters most to you)*

Use these answers to set .env values and configure the scheduler before proceeding. Don't leave them as defaults without asking.

---

## Prerequisites

- [ ] Vault Node, Context Node, and Intelligence Node installed
- [ ] Mobile Node installed (needs Telegram bot token)
- [ ] At least one data source collecting in reach/data/
- [ ] Python 3.10+ with venv active and requirements.txt installed

---

## .env Variables Required

| Variable | Description | Where to get it |
|----------|-------------|----------------|
| `GEMINI_API_KEY` | LLM for brief generation | aistudio.google.com → Get API Key |
| `ANTHROPIC_API_KEY` | Alternative LLM (if `BRIEF_LLM=claude`) | console.anthropic.com |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot | @BotFather on Telegram |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | @userinfobot on Telegram |
| `BRIEF_LLM` | `gemini` or `claude` (default: gemini) | Set in .env |
| `BRIEF_PRESET` | `founder` or `operator` (default: founder) | Set in .env |
| `DASHBOARD_METRIC` | Metric to chart (default: `youtube_subscribers`) | Set in .env |

---

## Files Installed

| File | What it does |
|------|-------------|
| `flow/brief/prompt.py` | Assembles mega-prompt from all data sources |
| `flow/brief/generate.py` | Calls Gemini or Claude, returns structured brief |
| `flow/brief/dashboard.py` | Generates chart image (matplotlib dark theme) |
| `flow/brief/deliver.py` | Sends brief + chart to Telegram |
| `flow/brief/daily_brief.py` | Orchestrator — runs all four in sequence |

---

## Setup Steps

1. **Add API keys to `.env`:**
   - `GEMINI_API_KEY` (recommended — cheapest option, ~$0.005/brief)
   - OR `ANTHROPIC_API_KEY` and set `BRIEF_LLM=claude`
   - `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` (from Mobile Node install)

2. **Test the prompt assembler:**
   ```bash
   python flow/brief/prompt.py
   ```
   Should print the assembled prompt (context + metrics + emails + meetings). Verify it looks right.

3. **Test brief generation:**
   ```bash
   python flow/brief/generate.py
   ```
   Should return a formatted brief. Takes 10–30 seconds.

4. **Test the dashboard image:**
   ```bash
   python flow/brief/dashboard.py
   ```
   Creates `flow/brief/dashboard.png`. Open it — should show a chart of your key metric.

5. **Test delivery:**
   ```bash
   python flow/brief/deliver.py
   ```
   Brief should appear in your Telegram within a few seconds.

6. **Run the full pipeline:**
   ```bash
   python flow/brief/daily_brief.py
   ```
   Full run: prompt → generate → chart → deliver → archive. Takes 30–60 seconds.
   Check `tuning/briefs/` — a `YYYY-MM-DD.md` file should appear.

7. **Schedule the daily run (7 AM):**

   **Windows (Task Scheduler):**
   - Import `flow/schedules/DailyBrief-generate.xml`
   - Or: create a task that runs `python flow/brief/daily_brief.py` at 7:00 AM daily

   **Mac/Linux (cron):**
   ```bash
   # Runs after collectors at 6:00 AM
   0 7 * * * cd /path/to/your-aios && .venv/bin/python flow/brief/daily_brief.py
   ```

---

## Validation

1. Run `python flow/brief/daily_brief.py` — completes without errors
2. Brief appears in Telegram with chart image attached
3. `tuning/briefs/YYYY-MM-DD.md` is created
4. Brief contains at least: executive summary, metrics snapshot, email digest

---

## Customizing the Brief

The brief format is defined in `flow/brief/generate.py` as a system prompt. Edit the `FOUNDER_PRESET` or `OPERATOR_PRESET` strings to add/remove sections or change the format.

Sections you can add:
- Google Calendar events for today (requires Calendar API)
- Slack channel digests (requires Slack API)
- CRM pipeline snapshot (requires CRM API)

---

## Next Steps

Install the Mobile Node if you haven't already (required for delivery):
```
/install node-installs/mobile-node
```

Install the Productivity Node for GTD task management:
```
/install node-installs/productivity-node
```

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | Initial release | Gemini + Claude options, founder + operator presets |
