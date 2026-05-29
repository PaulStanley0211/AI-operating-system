---
name: triage
description: Read Gmail, classify by the CLAUDE.md Email Profile, draft replies in Paul's voice into Gmail Drafts for review, and log time saved. Usage: /triage
user_invocable: true
trigger: /triage
version: 1.0.0
---

# /triage — Inbox Triage

## Step 1: Preconditions

Confirm `reach/auth/token.json` exists and its scopes include `gmail.compose`:
```bash
python -X utf8 -c "import json,sys; d=json.load(open('reach/auth/token.json')); sys.exit(0 if any('gmail.compose' in s for s in d.get('scopes',[])) else 1)" && echo "compose OK" || echo "NEEDS REAUTH"
```
If it prints `NEEDS REAUTH` or the file is missing, stop and tell the user:
"Gmail needs re-auth with compose scope. Run: `rm reach/auth/token.json && python reach/auth/gmail_auth.py`"

## Step 2: Load candidates (refresh first)

Run a Python snippet that refreshes the inbox and loads candidates:
```bash
python -X utf8 -c "import json; from actions.triage.emails import get_candidates; cands, refreshed = get_candidates(refresh=True); print('REFRESHED', refreshed); print(json.dumps(cands, ensure_ascii=False))"
```
- `REFRESHED False` means the live pull failed — continue on existing data and note it in your summary.
- Parse the JSON list of candidates (each: message_id, thread_id, date, sender, subject, body_preview).
- If the list is empty: report "Inbox clean, nothing to draft," still record a zero run (Step 6), and stop.

## Step 3: Classify each candidate

Apply the **Email Profile in `CLAUDE.md`** to each candidate. Assign exactly one:
- **ignore** — slipped past the pre-filter but is still noise per the profile.
- **gray-zone** — negotiations, declines, rejections, salary discussions, or anything sensitive. NEVER draft these.
- **draft** — any real human with a genuine purpose (recruiters, hiring managers, interview scheduling, application follow-ups, prospective clients, direct questions).

When unsure between draft and gray-zone, choose **gray-zone** (safer — Paul writes it himself).

## Step 4: Draft replies (for "draft" items only)

For each **draft** item, write a reply in Paul's voice using `context/voice/samples.md`:
- Warm and conversational, tight short sentences, polite not formal.
- Obey the banned-words list (no em dashes, no "delve into", "leverage", "robust", etc.).
- Sign-off: "Kind regards, Paul" for recruiters/hiring managers/clients; "Paul" for casual.
- Keep it short. Only address what the email actually asks.

## Step 5: Review table (approval gate)

Present ONE table to Paul and STOP for his decision. Do not create any drafts yet.

| # | From | Subject | Class | Action | Draft preview |
|---|------|---------|-------|--------|---------------|
| 1 | Paulina (Eraneos) | Re: your application | draft | will draft | "Hi Paulina, thanks for..." |
| 2 | Recruiter X | Salary expectations? | gray-zone | you write this | (sensitive — surfaced only) |

Ask: "Approve all drafts, pick numbers, edit any, or skip?" Wait for his answer.

## Step 6: Execute approved drafts + log

For each APPROVED draft, create the Gmail draft and record the action:
```bash
python -X utf8 -c "
import json, datetime
from actions.triage.gmail_draft import get_gmail_service, create_reply_draft
import sqlite3
svc = get_gmail_service()
# ITEMS is a JSON list of {thread_id,to,subject,body,in_reply_to,message_id} you fill in:
ITEMS = json.loads('''<JSON_HERE>''')
conn = sqlite3.connect('reach/data/intel.db')
for it in ITEMS:
    did = create_reply_draft(svc, it['thread_id'], it['to'], it['subject'], it['body'], it.get('in_reply_to'))
    conn.execute('INSERT OR IGNORE INTO triage_actions (message_id, classification, action, draft_id, run_date) VALUES (?,?,?,?,?)',
                 (it['message_id'], 'draft', 'drafted', did, datetime.date.today().isoformat()))
conn.commit(); conn.close(); print('drafts created:', len(ITEMS))
"
```
- Use the candidate's `message_id` as `in_reply_to` (it is the RFC Message-ID) and `to` = the candidate's sender.
- Also record `triage_actions` rows for ignore and gray-zone items (action = 'ignored' / 'surfaced', draft_id = NULL) so they are not re-processed next run. Do this with a similar INSERT.
```bash
python -X utf8 -c "
import json, sqlite3, datetime
conn = sqlite3.connect('reach/data/intel.db')
# NON_DRAFT: list of {message_id, classification, action} for ignore + gray-zone items
NON_DRAFT = json.loads('''<JSON_HERE>''')
for it in NON_DRAFT:
    conn.execute('INSERT OR IGNORE INTO triage_actions (message_id, classification, action, draft_id, run_date) VALUES (?,?,?,?,?)',
                 (it['message_id'], it['classification'], it['action'], None, datetime.date.today().isoformat()))
conn.commit(); conn.close(); print('non-draft actions recorded:', len(NON_DRAFT))
"
```
- If a single draft creation raises, report which one failed and continue the rest.

Then record the run and print the rollup:
```bash
python -X utf8 -c "from actions.triage.runlog import record_run, weekly_rollup; record_run(seen=SEEN, drafted=DRAFTED, surfaced=SURFACED, ignored=IGNORED); import json; print(json.dumps(weekly_rollup()))"
```
(Substitute the integer counts from this run.)

## Step 7: Summary

Print a short summary: drafts created (with where to find them, Gmail Drafts) and gray-zone items surfaced (so Paul writes them).

Then print the weekly rollup as a **transparent breakdown**, never a bare number. Use the keys from `weekly_rollup()`:

> This week: {drafts} drafts (~{draft_minutes} min) + {scans} daily scans (~{triage_minutes} min) = ~{total_minutes} min saved. Noise filtered: {noise_filtered} emails.

Every minute traces to a real action: `draft_minutes` is drafts × 6 (compose time), `triage_minutes` is scans × 3 (inbox scan skipped, credited only on runs that saw email). The `noise_filtered` count is the raw evidence behind the number. Keep it tight.
