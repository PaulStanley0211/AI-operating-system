---
name: audit
description: Grade your CRAFT environment layer by layer (C/R/A/F/T). Produces a score out of 100 and a gap report. Saves to tuning/audits/. Run weekly to track maturity.
user_invocable: true
trigger: /audit
version: 1.0.0
---

# /audit — CRAFT Environment Audit

## Step 1: Run All Checks

Check every item below. For each check, assign the listed points if it passes, 0 if it fails.

### C — Context (max 20 pts)

| # | Check | Points | How to check |
|---|-------|--------|-------------|
| C1 | `CRAFT.md` exists and has no `[FILL IN]` remaining in identity/business sections | 5 | Read CRAFT.md, look for [FILL IN] |
| C2 | `context/voice/samples.md` exists with 3+ samples | 5 | Check file exists, count samples |
| C3 | Email profile in CRAFT.md has at least 3 rules per bucket | 5 | Read email profile section |
| C4 | At least one file exists in `context/references/` | 3 | Check directory |
| C5 | `context/strategy.md` exists and was modified within 90 days | 2 | Check file modified date |

### R — Reach (max 20 pts)

| # | Check | Points | How to check |
|---|-------|--------|-------------|
| R1 | `reach/data/data.db` exists | 3 | Check file exists |
| R2 | At least one metric source has data from within 2 days | 5 | Query latest date from any table |
| R3 | `reach/metrics.md` exists and was modified within 2 days | 4 | Check file and modified date |
| R4 | `reach/data/intel.db` exists | 3 | Check file exists |
| R5 | Emails table in intel.db has records from within 7 days | 3 | Query emails table |
| R6 | Meetings table in intel.db has any records | 2 | Query meetings table |

### A — Actions (max 20 pts)

| # | Check | Points | How to check |
|---|-------|--------|-------------|
| A1 | `.claude/commands/analyze.md` exists | 3 | Check file |
| A2 | `.claude/commands/plan.md` exists | 3 | Check file |
| A3 | `.claude/commands/build.md` exists | 3 | Check file |
| A4 | `.claude/commands/email-triage.md` exists | 5 | Check file |
| A5 | `.claude/commands/pulse.md` exists | 3 | Check file |
| A6 | Any additional skills beyond the 5 listed above | 3 | Count files in .claude/commands/ |

### F — Flow (max 20 pts)

| # | Check | Points | How to check |
|---|-------|--------|-------------|
| F1 | Any file exists in `flow/schedules/` (scheduler configured) | 5 | Check directory |
| F2 | At least one file exists in `tuning/briefs/` | 5 | Check directory |
| F3 | `flow/bot/main.py` exists | 5 | Check file |
| F4 | All 8 GTD files exist in `flow/gtd/` | 5 | Check files: inbox, projects, next-actions, waiting-for, someday-maybe, areas, dashboard, review-checklist |

### T — Tuning (max 20 pts)

| # | Check | Points | How to check |
|---|-------|--------|-------------|
| T1 | `tuning/changelog.md` has at least 2 entries | 3 | Read file, count ## date sections |
| T2 | `tuning/audits/` directory exists | 2 | Check directory |
| T3 | At least one prior audit exists in `tuning/audits/` | 5 | Check for files |
| T4 | `.claude/commands/tune.md` exists | 5 | Check file |
| T5 | At least one completed plan exists in `tuning/plans/` | 5 | Check for files with Status: Complete |

## Step 2: Calculate Scores

Tally points for each layer. Assign letter grades:
- 18–20: A
- 15–17: B
- 11–14: C
- 7–10: D
- 0–6: F

## Step 3: Produce the Report

```markdown
## CRAFT Audit — [date]

### Overall Score: [total]/100

| Layer | Score | Max | Grade |
|-------|-------|-----|-------|
| C — Context | [c] | 20 | [grade] |
| R — Reach | [r] | 20 | [grade] |
| A — Actions | [a] | 20 | [grade] |
| F — Flow | [f] | 20 | [grade] |
| T — Tuning | [t] | 20 | [grade] |
| **Total** | **[total]** | **100** | **[overall]** |

### Top Gaps (prioritized by impact)

1. **[Layer] — [score]/20:** [What's missing and why it matters]
   → Fix: [specific action to take]

2. **[Layer] — [score]/20:** [What's missing]
   → Fix: [specific action]

3. **[Layer if applicable]**

### What's Working
- [Layer]: [brief note on what's strong]

### Score History
[If prior audits exist in tuning/audits/, show score trend]
[date]: [score]/100
[date]: [score]/100
[today]: [score]/100

### Recommended Next Action
[Single most impactful thing to do next. End with the specific command to run.]
```

## Step 4: Save the Report

Save the full report to: `tuning/audits/[YYYY-MM-DD]-audit.md`

Append to `tuning/changelog.md`:
```
## [date]
- Audit run: [score]/100. Top gap: [layer].
```

Print: "Audit saved to tuning/audits/[filename].md"

## Behavior Rules

- Be honest. Zero points means zero — don't give partial credit for half-done items.
- The gap list must be prioritized by impact, not just score. A missing email-triage skill (A) is higher impact than a missing Fireflies connection (R).
- Always end with exactly one recommended next action.
