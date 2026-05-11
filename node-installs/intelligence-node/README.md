# Intelligence Node

> Layer: R (Reach)
> Connects your data sources. Collects metrics daily. Gives the AI eyes on your business.

---

## What It Is

The Intelligence Node is your data layer. It installs collectors that pull numbers from your actual business tools — YouTube, Stripe, Gmail, Outlook, Fireflies — and store everything in a local SQLite database. Once it's running, your AI can see what's actually happening in your business, not just what you tell it.

A scheduled job runs the collectors automatically every morning so your data is always fresh before you start work.

---

## What It Does

- Installs data collectors for each of your connected sources
- Creates a local SQLite database (`reach/data/data.db`) for business metrics
- Creates a second database (`reach/data/intel.db`) for emails and meeting transcripts
- Generates `reach/metrics.md` — a formatted snapshot of all your current numbers
- Schedules a daily run (6 AM by default) so collection happens automatically

**Supported data sources:**

| Source | What gets collected |
|--------|-------------------|
| YouTube | Subscribers, total views, video count, 30-day performance |
| Stripe | MRR, ARR, active subscribers |
| Gmail | Inbox emails (noise-filtered, last 24 hours) |
| Outlook / Microsoft 365 | Same as Gmail, via Microsoft Graph API |
| Fireflies | Full meeting transcripts, summaries, action items |
| FX Rates | Currency exchange rates |

You only set up the sources you actually use. Claude skips the rest.

---

## How to Install

With Vault and Context nodes already installed, run:
```
/install node-installs/intelligence-node
```

Claude will ask you 5 setup questions before touching anything:
1. Do you have a YouTube channel to track?
2. Do you use a payment processor for revenue — Stripe, something else, or none yet?
3. Which email do you use — Gmail, Outlook, both, or something else?
4. Do you use a meeting transcription tool like Fireflies or Otter?
5. Are you on Windows, Mac, or Linux? (for scheduler setup)

After your answers, Claude will tell you exactly what it will connect and what it will skip. Then it sets up only what you confirmed.

---

## How to Know It's Working

After install, run:
```bash
python reach/collectors/collect.py
```

You should see each configured collector complete with a count of rows collected. Then run:
```bash
python reach/generate_metrics.py
```

Open `reach/metrics.md` — it should show real numbers from your connected sources with today's date.

In Claude Code, run:
```
/pulse
```

If `/pulse` returns actual numbers (not placeholder text), the Intelligence Node is working.

---

## What to Expect

The initial setup requires navigating 1–3 external developer consoles to get API keys. This is the most technically involved part of the entire AIOS install. Expect 30–60 minutes if it's your first time doing OAuth setup for Gmail or creating a YouTube API key.

Once it's configured, you won't need to touch it again. The daily collection job runs silently in the background. Your metrics stay current automatically.

**Gmail/Outlook auth requires a one-time browser sign-in.** You'll run a script, a browser window opens, you authorize, and it saves a token. After that, collection is fully automatic.

---

## What You Have to Do Yourself

| Task | Notes |
|------|-------|
| Get a YouTube API key | Google Cloud Console → Enable YouTube Data API v3 → Credentials |
| Get a Stripe restricted key | Stripe Dashboard → Developers → API Keys (read-only is fine) |
| Create Gmail OAuth credentials | Google Cloud Console → OAuth 2.0 client ID |
| Run Gmail auth script once | Browser sign-in, saves token — then automatic forever |
| Set up Azure app for Outlook | Azure Portal → App registrations → Mail.Read permission |
| Run Outlook device code auth once | Follow prompt, sign in — then automatic forever |
| Get Fireflies API key | app.fireflies.ai → Settings → API |
| Set up Task Scheduler / cron | Claude provides the exact command and timing |

You only do the tasks for sources you confirmed in setup. If you said no to Stripe, you do nothing for Stripe.

---

## Next Step

Once Intelligence is running:
```
/install node-installs/coffee-debrief-node
```
