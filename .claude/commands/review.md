---
name: review
description: Run the 4-phase weekly GTD review. GET CLEAR → GET CURRENT → GET CREATIVE → REBUILD. Recommended every Friday. Takes 30–60 minutes.
user_invocable: true
trigger: /review
version: 1.0.0
---

# /review — Weekly GTD Review

## Opening

Print:
```
## Weekly Review — [today's date]

4 phases. Estimated time: 30–60 minutes.
Let's start.
```

---

## Phase 1 — GET CLEAR

**Goal:** Empty all inboxes. Nothing captured outside the system.

1. Run `/process` on `flow/gtd/inbox.md`. (Call the /process skill directly.)
2. Ask: "Any items in a physical notebook, notes app, or Telegram that haven't been captured? Add them to inbox.md, then I'll process them."
3. If new items are added, run `/process` again.

**Phase 1 complete when:** `flow/gtd/inbox.md` is empty.

Print: `✅ Phase 1 — GET CLEAR complete. Inbox: 0 items.`

---

## Phase 2 — GET CURRENT

**Goal:** Every list is accurate and current.

### Projects Review
Read `flow/gtd/projects.md`. For each active project:
- Does it have a valid next action in `flow/gtd/next-actions.md`? If not, add one now.
- Is it actually still active? If stalled: mark "On hold". If done: mark "Complete" and remove from active.
- Ask: "Any project here that's actually done or should be paused?"

### Next Actions Review
Read `flow/gtd/next-actions.md`. Walk through each context group:
- Are any items done? Mark them.
- Are any items no longer relevant? Remove them.
- Any item sitting there 3+ weeks without movement? Surface it — is it really a project? Is it someday/maybe?

### Waiting For Review
Read `flow/gtd/waiting-for.md`. For each item:
- Has it been received? Remove it.
- Is it overdue? Flag it: "This item from [person] was expected by [date] — want to follow up?"

### Someday/Maybe
Read `flow/gtd/someday-maybe.md`. Quick scan:
- Anything worth activating this week? If yes, move to projects or next-actions.

**Phase 2 complete when:** All four lists have been reviewed and updated.

Print:
```
✅ Phase 2 — GET CURRENT complete.
Projects: [X active, Y completed, Z on hold]
Next actions: [A removed, B added]
Waiting for: [C overdue flagged]
```

---

## Phase 3 — GET CREATIVE

**Goal:** Catch anything the task-level lists might be missing.

Read `flow/gtd/areas.md`. For each area of responsibility:
- "Is there something in [area] that needs attention right now that isn't in the system?"
- If yes, add to inbox and run `/process` on it.

Read the last 3 files in `tuning/briefs/` (if they exist). Scan for:
- Signals that keep recurring
- Action items that appeared but weren't captured
- Anything that should become a project

Ask: "Is there anything you've been worried about that isn't in the system anywhere?"

Print: `✅ Phase 3 — GET CREATIVE complete.`

---

## Phase 4 — REBUILD

**Goal:** A clear, accurate picture of the week ahead.

1. Run: `python flow/refresh_dashboard.py`
2. Read the regenerated `flow/gtd/dashboard.md`
3. Ask: "What's the single most important project for the coming week?"
4. Confirm that project has a clear next action. If not, add one now.
5. Optional: ask "Want to write a brief intention for the week? I'll add it to the dashboard."

Print:
```
✅ Phase 4 — REBUILD complete.
Dashboard refreshed.
This week's focus: [project name]

---

## Review Complete — [date]

Clear: ✅ | Current: ✅ | Creative: ✅ | Rebuilt: ✅

See you next Friday.
```

---

## Behavior Rules

- Keep momentum. Don't get stuck on any single item — decisions are made in seconds, not minutes.
- The review is not a planning session. Process and clarify; save deep thinking for later.
- Run `/process` automatically in Phase 1 — don't ask for permission.
- If the user gets distracted or wants to stop, print what's been completed and where to resume.
