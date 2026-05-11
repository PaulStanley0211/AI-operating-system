---
name: email-triage
description: Classify inbox emails into ignore / draft / auto-respond using the email profile in CRAFT.md. Reads from reach/data/intel.db or accepts pasted emails. Usage: /email-triage or /email-triage [days]
user_invocable: true
trigger: /email-triage
version: 1.0.0
---

# /email-triage — Inbox Triage

This skill classifies emails into three buckets using the email profile defined in CRAFT.md.

## Step 1: Read the Email Profile

Read `CRAFT.md` and extract the Email Profile section:
- Ignore rules
- Draft rules
- Auto-respond rules
- Auto-respond template text

## Step 2: Get Emails

**Mode A — Connected (intel.db exists):**

Query `reach/data/intel.db` for emails:
```python
import sqlite3
from datetime import datetime, timedelta

days = 1  # default; use the number if user passed /email-triage 3
cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

conn = sqlite3.connect("reach/data/intel.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("""
    SELECT source, date, sender, subject, body_preview 
    FROM emails 
    WHERE date >= ? 
    ORDER BY date DESC
""", (cutoff,))
emails = [dict(r) for r in c.fetchall()]
conn.close()
```

**Mode B — Paste (intel.db doesn't exist or is empty):**

Say: "No email database found. Paste your emails below in any format — one per block — and I'll triage them."

Wait for the user to paste, then proceed with those emails.

## Step 3: Classify Each Email

For each email, apply the rules from CRAFT.md in this order:

1. **Ignore** — match against ignore rules. If any rule applies → Ignore bucket.
2. **Auto-respond** — match against auto-respond rules. If any rule applies → Auto-respond bucket.
3. **Draft** — everything else that needs a response → Draft bucket.

Classification signals to look for:
- **Ignore:** newsletter footers, unsubscribe links, from a known notification domain, no personal addressing
- **Auto-respond:** templated pitch language, cold outreach patterns, first-contact from unknown senders with a sales ask
- **Draft:** personal addressing, existing relationship signals, a specific question requiring judgment

## Step 4: Draft Replies

For every email in the **Draft** bucket, write a reply:

- Write in the voice defined in CRAFT.md voice section
- Reference `context/voice/samples.md` if it exists — match the tone
- Get to the point in the first sentence. No filler openers.
- Keep it concise — draft replies should be ready to send after a 10-second review.
- Sign with the name from CRAFT.md

## Step 5: Stage Auto-Responses

For every email in the **Auto-respond** bucket:
- Use the auto-respond template from CRAFT.md
- Personalize only the sender name if clearly available
- Mark as "staged — review before sending" unless the user has explicitly set these to auto-send

## Step 6: Produce the Triage Report

```
## Email Triage — [date]
[Total] emails processed | [X] ignored | [Y] in draft | [Z] auto-respond

---

### 🗑️ Ignore ([X])
[list each: sender — subject (reason)]

---

### ✍️ Draft Queue ([Y])

**From:** [sender]
**Subject:** [subject]
**Summary:** [one-line: what they're actually asking]

**Draft reply:**
> [Full draft, ready to review]

---
[repeat for each]

---

### ⚡ Auto-Respond ([Z])

**From:** [sender]
**Subject:** [subject]
**Response staged:**
> [Template text]

---
```

## Behavior Rules

- Never assume — if you can't confidently classify an email, put it in Draft
- The draft should sound like the user wrote it, not like a generic AI email
- If no emails are found in the database, say so clearly and offer Paste mode
- Do not send anything. This skill stages and drafts — the user takes action.
