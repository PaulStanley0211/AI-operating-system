# Coffee Debrief Node

> Layer: A (Actions)
> Synthesizes everything into a morning brief and delivers it to your phone by 7 AM.

---

## What It Is

The Coffee Debrief Node takes everything the Intelligence Node collects — your metrics, emails, and meeting transcripts — and turns it into a structured morning intelligence report. It generates a chart of your key metric, then delivers the full brief to your Telegram by the time you sit down with coffee.

By the time you open your phone in the morning, you already know what happened yesterday and what needs your attention today.

---

## What It Does

- Assembles a mega-prompt from all your data sources: context, metrics, emails, and meeting summaries
- Calls an AI (Gemini or Claude) to generate a structured daily brief
- Creates a chart image of your most important metric (dark theme, 800x400)
- Sends the brief and chart to your Telegram
- Archives each brief to `tuning/briefs/YYYY-MM-DD.md` so you can review past signals
- Runs automatically at 7 AM every day (after collectors finish at 6 AM)

**Brief sections (Founder preset):**
- Executive summary — 3-5 sentence overview of yesterday
- Key signals — what changed, what moved, what to watch
- Metrics snapshot — your numbers vs. yesterday / last week
- Email digest — the emails that actually matter, filtered from noise
- Today's focus — 1-3 things that deserve your attention

---

## How to Install

With Intelligence Node already installed, run:
```
/install node-installs/coffee-debrief-node
```

Claude will ask you 5 setup questions:
1. Which AI model to use for brief generation — Gemini (recommended, ~$0.005/brief) or Claude (~$0.03/brief)
2. How much detail you want — Founder preset (3–5 min read) or Operator preset (8–10 min read)
3. The single most important metric in your business right now
4. What time you want the brief delivered each morning
5. Anything specific you always want the brief to surface

Your answers configure `.env` and the brief system prompt before anything runs.

---

## How to Know It's Working

Run the full pipeline manually:
```bash
python flow/brief/daily_brief.py
```

This should complete in 30–60 seconds and produce:
- A brief in your Telegram (with chart image attached)
- A new file at `tuning/briefs/YYYY-MM-DD.md`

Check the brief in Telegram. It should include:
- [ ] An executive summary paragraph
- [ ] At least one metrics section with real numbers
- [ ] An email digest (if Gmail/Outlook is connected)
- [ ] A chart image showing your key metric

If all four are present, the Coffee Debrief Node is working.

---

## What to Expect

The first brief might feel generic. The AI is calibrated to your context and data, but it gets better as more data accumulates. By week two, the brief is noticeably more relevant.

Briefs are archived in `tuning/briefs/`. You can ask Claude to summarize trends across the last 7 days, compare week-over-week, or find when a specific metric changed. The archive becomes a searchable record of what was happening in your business.

**Gemini is the recommended choice.** It's fast, cheap (~$0.005 per brief), and produces excellent quality. Claude Haiku is a good alternative if you already have an Anthropic API key and want to minimize external services.

---

## What You Have to Do Yourself

| Task | Notes |
|------|-------|
| Get a Gemini API key | aistudio.google.com → Get API Key → free tier available |
| OR get an Anthropic API key | console.anthropic.com (if using Claude instead) |
| Mobile Node must be installed first | Telegram bot token is required for delivery |
| Set the delivery time in Task Scheduler / cron | Claude provides the exact command during setup |

The Mobile Node (Telegram bot) must be installed before the Coffee Debrief can deliver to your phone. If you haven't done that yet, install Mobile Node first.

---

## Next Step

Once Coffee Debrief is running:
```
/install node-installs/mobile-node
```

Or if Mobile Node is already installed, move to:
```
/install node-installs/productivity-node
```
