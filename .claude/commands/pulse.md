---
name: pulse
description: On-demand snapshot of current business metrics. Queries reach/data/data.db live. Usage: /pulse or /pulse [source] to filter by source (youtube, stripe, etc.)
user_invocable: true
trigger: /pulse
version: 1.0.0
---

# /pulse — Live Metrics Snapshot

## Step 1: Check Intelligence Node

Check if `reach/data/data.db` exists. If not:
```
Intelligence Node not installed yet. Set it up first to connect your data sources.
See: node-installs/intelligence-node/INSTALL.md
```
Stop here.

## Step 2: Parse Source Filter

If the user passed a source (e.g., `/pulse youtube`, `/pulse stripe`), filter results to that source only.

## Step 3: Query the Database

Write and run a Python script to query `reach/data/data.db`. Query the latest row from each table that exists:

```python
import sqlite3, os
from datetime import datetime, date

DB_PATH = "reach/data/data.db"
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Check which tables exist
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]

results = {}

if "youtube_daily" in tables:
    c.execute("SELECT * FROM youtube_daily ORDER BY date DESC LIMIT 1")
    results["youtube"] = dict(c.fetchone() or {})

if "youtube_videos" in tables:
    c.execute("""
        SELECT title, views, likes FROM youtube_videos 
        WHERE date >= date('now', '-30 days')
        ORDER BY views DESC LIMIT 3
    """)
    results["youtube_videos"] = [dict(r) for r in c.fetchall()]

if "stripe_daily" in tables:
    c.execute("SELECT * FROM stripe_daily ORDER BY date DESC LIMIT 1")
    results["stripe"] = dict(c.fetchone() or {})

if "fx_rates" in tables:
    c.execute("SELECT currency, rate_from_usd, date FROM fx_rates ORDER BY date DESC, currency")
    results["fx"] = [dict(r) for r in c.fetchall()]

conn.close()
print(results)
```

## Step 4: Format the Output

Produce a clean snapshot table. Only show sections where data exists.

```
## Pulse — [current datetime]

### YouTube (@[handle from CRAFT.md])
| Metric | Value | As Of |
|--------|-------|-------|
| Subscribers | [value] | [date] |
| Total Views | [value] | [date] |
| Views (30d) | [value] | [date] |

**Top videos (30d):**
1. "[title]" — [views] views
2. ...

### Revenue (Stripe)
| Metric | Value |
|--------|-------|
| MRR | $[value] |
| Active subscribers | [value] |

### Data Freshness
| Source | Last collected | Status |
|--------|---------------|--------|
| youtube_daily | [date] | ✅ / ⚠️ stale |
| stripe_daily | [date] | ✅ / ⚠️ stale |
```

## Step 5: Freshness Flags

For each source: compare the `date` field to today.
- Same day or yesterday → ✅ Fresh
- 2–3 days ago → ⚠️ [N] days ago
- 4+ days ago → 🔴 Stale — run your collector

If any source is stale, add at the bottom:
```
To refresh: python reach/collectors/collect.py
Or: /pulse fresh (runs collectors first)
```

## Variation: /pulse fresh

If the user runs `/pulse fresh`:
1. Print: "Running collectors..."
2. Execute: `python reach/collectors/collect.py`
3. Then proceed with the normal pulse output.
