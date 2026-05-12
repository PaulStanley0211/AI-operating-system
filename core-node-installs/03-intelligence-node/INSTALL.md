# Intelligence Node — Install Guide
<!-- v1.0.0 -->

> Layer: R (Reach)
> Connects your data sources. Collects metrics daily. Makes your business data visible to the AI.

---

## What This Node Does

Installs data collectors that pull from your business APIs on a schedule, stores everything in a local SQLite database, and generates `reach/metrics.md` automatically. After this node, the AI can see your live business data and `/pulse` returns real numbers.

---

## Setup Questions

Ask these before doing anything. Each answer determines which collectors get set up and which get skipped.

1. **Do you have a YouTube channel you want to track?**
   *(Yes = set up YouTube collector. No = skip entirely — don't ask for a YouTube API key)*

2. **Do you use a payment processor for revenue? Which one — Stripe, something else, or none yet?**
   *(Stripe = set up Stripe collector. Something else = note it, skip for now. None = skip)*

3. **Which email do you use for business — Gmail, Outlook/Microsoft 365, both, or something else?**
   *(Sets up the relevant email collector. Both = set up both. Something else = skip email collection for now)*

4. **Do you use any meeting transcription tool — like Fireflies, Otter, or something similar?**
   *(Fireflies = set up Fireflies collector. Other = mention it's not supported yet. None = skip)*

Only install collectors for sources the user confirmed. Don't ask for API keys for services they don't use.
After collecting answers, show a summary: "We'll connect: [list]. Skipping: [list]."

Scheduling the collector to run automatically each morning is set up in the Mobile Node (Flow layer) — skip that here.

---

## Prerequisites

- [ ] Vault Node and Context Node installed
- [ ] Python 3.10+ with virtual environment active
- [ ] `pip install -r requirements.txt` completed
- [ ] At least one API key from the list below

---

## .env Variables Required

Add the ones matching your connected sources. Start with just one — YouTube is easiest.

| Variable | Source | Where to get it |
|----------|--------|----------------|
| `YOUTUBE_API_KEY` | YouTube Data API v3 | console.cloud.google.com → Enable YouTube Data API v3 → Credentials → API Key |
| `YOUTUBE_CHANNEL_ID` | Your channel ID | youtube.com → your channel → URL contains the ID |
| `STRIPE_SECRET_KEY` | Stripe | dashboard.stripe.com → Developers → API Keys → Create restricted key (read-only) |
| `GMAIL_CREDENTIALS_PATH` | Gmail OAuth | console.cloud.google.com → OAuth 2.0 credentials |
| `OUTLOOK_CLIENT_ID` | Azure AD app | portal.azure.com → App registrations |
| `FIREFLIES_API_KEY` | Fireflies.ai | app.fireflies.ai → Settings → API |
| `OPEN_EXCHANGE_RATES_APP_ID` | FX rates | openexchangerates.org → Free account |

---

## Files Installed

| File | What it does |
|------|-------------|
| `reach/collectors/db.py` | Database setup, table creation, connection helpers |
| `reach/collectors/config.py` | Loads .env vars as constants |
| `reach/collectors/collect.py` | Orchestrator — runs all collectors in sequence |
| `reach/collectors/youtube.py` | YouTube channel stats + video performance |
| `reach/collectors/stripe.py` | Stripe MRR, ARR, subscriber counts |
| `reach/collectors/gmail.py` | Gmail inbox (last N days, noise-filtered) |
| `reach/collectors/outlook.py` | Outlook inbox (same, via Graph API) |
| `reach/collectors/fireflies.py` | Meeting transcripts and summaries |
| `reach/auth/gmail_auth.py` | One-time Gmail OAuth2 setup |
| `reach/auth/outlook_auth.py` | One-time Outlook device code auth |
| `reach/generate_metrics.py` | Queries DB → writes reach/metrics.md |

---

## Setup Steps

1. **Create the database directories:**
   ```bash
   mkdir -p reach/data reach/auth
   ```

2. **Initialize the databases:**
   ```bash
   python reach/collectors/db.py
   ```
   Creates `reach/data/data.db` and `reach/data/intel.db` with all tables.

3. **Connect YouTube** (start here — easiest, requires only an API key):
   - Add `YOUTUBE_API_KEY` and `YOUTUBE_CHANNEL_ID` to `.env`
   - Test: `python reach/collectors/youtube.py`
   - Expected: "YouTube: collected 1 row. Subscribers: [your count]"

4. **Connect Gmail** (optional):
   - Get OAuth2 credentials JSON from Google Cloud Console
   - Save as `reach/auth/gmail_credentials.json`
   - Run once: `python reach/auth/gmail_auth.py`
   - Follow the browser prompt, authorize, done.
   - Test: `python reach/collectors/gmail.py`

5. **Connect Outlook** (optional):
   - Create an app in Azure AD with Mail.Read permission
   - Add `OUTLOOK_CLIENT_ID` and `OUTLOOK_TENANT_ID` to `.env`
   - Run once: `python reach/auth/outlook_auth.py`
   - Follow the device code prompt, sign in, done.
   - Test: `python reach/collectors/outlook.py`

6. **Connect Fireflies** (optional):
   - Add `FIREFLIES_API_KEY` to `.env`
   - Test: `python reach/collectors/fireflies.py`

7. **Connect FX rates** (optional — good "hello world" collector):
   - Add `OPEN_EXCHANGE_RATES_APP_ID` to `.env`
   - Or use the free endpoint that requires no key (limited currencies)
   - Test: `python reach/collectors/fx_rates.py`

8. **Run the full collector:**
   ```bash
   python reach/collectors/collect.py
   ```
   Should run all configured collectors and print a summary.

9. **Generate your metrics file:**
   ```bash
   python reach/generate_metrics.py
   ```
   Opens `reach/metrics.md` — should show your connected data.

> Scheduling the collector to run automatically each morning is covered in the Mobile Node. For now, run it manually to verify everything works.

---

## Validation

1. Run `python reach/collectors/collect.py` — should complete without errors
2. Run `python reach/generate_metrics.py` — `reach/metrics.md` should appear with real numbers
3. Run `/start` in Claude Code — metrics should appear in the session summary
4. Run `/pulse` — should return a live snapshot

---

## Next Steps

Install the Mobile Node to get phone access and set up your Telegram command center:
```
/install core-node-installs/04-mobile-node
```

Then install the Coffee Debrief Node to receive your morning brief in Telegram:
```
/install core-node-installs/05-coffee-debrief-node
```

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | Initial release | YouTube + Stripe + Gmail + Outlook + Fireflies + FX |
