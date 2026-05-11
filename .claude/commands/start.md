---
name: start
description: Initialize a new session. Loads CRAFT.md, context files, current metrics, and GTD state. Run this at the start of every session.
user_invocable: true
trigger: /start
version: 1.0.0
---

# /start — Session Initialization

Read the following files in order. After reading, produce the session summary below.

## Files to Read

1. `CRAFT.md` — identity, business, strategy, email profile, working preferences
2. `context/strategy.md` — current quarter priorities (if file exists)
3. `reach/metrics.md` — latest metrics snapshot (if file exists)
4. `flow/gtd/dashboard.md` — GTD state (if file exists)
5. Find the most recent file in `tuning/briefs/` — yesterday's signal (if any exist)

If a file doesn't exist, skip it silently. Do not mention missing files unless the absence is worth flagging.

## Session Summary Format

Produce exactly this structure:

```
## Session Ready — [today's date]

### Who I'm Working With
[Name], [role] at [business name]. [One sentence: what the business does.]

### Business State
[2–3 bullet points — most important numbers from reach/metrics.md. Skip if no metrics file.]

### Current Priorities
[2–3 bullet points from CRAFT.md strategy section or context/strategy.md]

### GTD State
[Inbox count] in inbox | [Project count] active projects | Top next action: [first @me item]
[Skip this section if Productivity Node not installed]

### Yesterday's Signal
[One sentence from the most recent brief — the single most important thing.]
[Skip this section if no briefs exist yet]

Ready. What are we working on?
```

## Freshness Check

After producing the summary, check `reach/metrics.md` last-modified date if the file exists.
- If metrics are more than 2 days old: add a note — "Metrics last updated [X] days ago — run `/pulse` to refresh."
- If metrics are more than 7 days old: flag it clearly — these are stale.

## Behavior

- Keep the summary scannable. The user reads it in 20 seconds.
- Do not list all available commands — the user knows them from CRAFT.md.
- Do not summarize what you just read — synthesize it.
- Match the working preferences set in CRAFT.md for format and length.
