# Productivity Node — Install Guide
<!-- v1.0.0 -->

> Layer: F (Flow)
> Installs a GTD task management system. The AI can process your inbox, route actions, and run weekly reviews.

---

## What This Node Does

Creates a file-based GTD system in `flow/gtd/`. The AI can capture tasks, process them through the decision tree with `/process`, and run a complete weekly review with `/review`. Also installs mobile capture via the Telegram bot (if Mobile Node is installed).

---

## Prerequisites

- [ ] Vault Node installed
- [ ] Python 3.10+ with venv active (for dashboard refresh script)
- [ ] Mobile Node installed (optional — enables Telegram /capture)

---

## .env Variables Required

None required for core install.

---

## Files Installed

| File | What it does |
|------|-------------|
| `flow/gtd/inbox.md` | Raw capture bucket |
| `flow/gtd/projects.md` | Master project list by area |
| `flow/gtd/next-actions.md` | Next actions by context tag |
| `flow/gtd/waiting-for.md` | Delegated items and owners |
| `flow/gtd/someday-maybe.md` | Future ideas and commitments |
| `flow/gtd/areas.md` | Areas of responsibility |
| `flow/gtd/dashboard.md` | Auto-generated operational hub |
| `flow/gtd/review-checklist.md` | Weekly review protocol |
| `flow/refresh_dashboard.py` | Reads GTD files → regenerates dashboard.md |
| `flow/inbox_writer.py` | Appends items to inbox.md programmatically |

---

## Setup Steps

1. **Verify files exist:**
   All GTD files ship with the repo. Check `flow/gtd/` contains all 8 markdown files.

2. **Customize `flow/gtd/areas.md`:**
   Open the file and replace the default areas with your actual areas of responsibility.
   Example areas: Business, Content, Finance, Personal, Operations

3. **Customize context tags in `flow/gtd/next-actions.md`:**
   The default tags are `@me`, `@claude`, `@calls`, `@errands`, `@waiting`.
   Add or rename tags to match how you work. Update `flow/gtd/review-checklist.md` to match.

4. **Add your first 3 real projects:**
   Open `flow/gtd/projects.md`. Add 3 real active projects from your head.
   Format:
   ```markdown
   ### [Project Name]
   - **Outcome:** What done looks like
   - **Status:** Active
   - **Next action:** [one concrete next step]
   ```

5. **Capture anything on your mind to inbox.md:**
   Open `flow/gtd/inbox.md` and write down everything that's been on your mind.
   One item per line. Don't organize — just capture.

6. **Run your first `/process`:**
   In Claude Code, type `/process`. Walk through the decision tree until inbox is at zero.

7. **Generate the dashboard:**
   ```bash
   python flow/refresh_dashboard.py
   ```
   Open `flow/gtd/dashboard.md` — should show project count, next actions, etc.

8. **Add Telegram capture** (if Mobile Node installed):
   Add this handler to `flow/bot/main.py`:
   ```python
   # In the message handler, check for /capture prefix:
   if text.startswith('/capture '):
       item = text[9:]
       os.system(f'python flow/inbox_writer.py "{item}"')
       await update.message.reply_text(f"Captured: {item}")
   ```
   Now send `/capture [anything]` to the bot to add items to inbox.md from your phone.

9. **Schedule weekly review:**
   Block 45–60 minutes every Friday. In Claude Code, type `/review`.
   The habit is the system — without weekly reviews, GTD stops working within 2–3 weeks.

---

## Validation

1. Run `/process` with at least 3 items in inbox.md → inbox reaches zero, items appear in next-actions or projects
2. Run `python flow/refresh_dashboard.py` → `flow/gtd/dashboard.md` updates with correct counts
3. Run `/review` → all 4 phases complete, dashboard refreshes at the end
4. (If Mobile Node installed) Send `/capture test item` to bot → appears in inbox.md

---

## Recommended Rhythm

| Frequency | Action |
|-----------|--------|
| Daily | Capture anything new to inbox.md |
| When inbox has items | Run `/process` |
| Weekly (Friday) | Run `/review` |
| After any GTD update | Run `python flow/refresh_dashboard.py` |

---

## Next Steps

Once all nodes are installed, run your first audit:
```
/audit
```

Then set up the tuning rhythm:
```
/tune
```

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | Initial release | GTD system + dashboard + Telegram capture |
