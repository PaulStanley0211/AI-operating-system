---
name: audit
description: Grade your CRAFT environment layer by layer (C/R/A/F/T). Produces a score out of 100 and a gap report. Saves to tuning/audits/. Run weekly to track maturity.
user_invocable: true
trigger: /audit
version: 2.0.0
---

# /audit — CRAFT Environment Audit

> **Rubric v2** — adapted to *this* project (a solo-engineer portfolio/proof AIOS focused on inbox triage), not the generic running-business template. Each layer mixes **Foundation (F)** checks — is the capability built? ratchets up and stays — with **Maturity (M)** checks — is it actually used and deepening? This is what makes the score climb honestly week over week instead of flatlining once things exist. A few Maturity checks are freshness-based and will dip if the system goes unused; that is intentional.

## Step 1: Run All Checks

Check every item. Assign the listed points if it passes, 0 if it fails. Be honest — zero means zero. Run the verification literally; do not assume.

For DB checks use `python -X utf8` (the repo is on Windows; this avoids cp1252 crashes). Email/run dates: "within N days" is measured against today.

### C — Context (max 20 pts)

| # | Check | Pts | Type | How to check |
|---|-------|-----|------|-------------|
| C1 | `CLAUDE.md` exists; identity, business, and strategy sections are filled (no blank `[FILL IN]` fields — the instructional comment near the top does not count) | 4 | F | Read CLAUDE.md; confirm no unfilled `[FILL IN]` placeholders in those sections |
| C2 | Email Profile in CLAUDE.md defines all four buckets (ignore / draft / auto-respond / gray-zone) with rules | 3 | F | Read the Email Profile section |
| C3 | `context/voice/samples.md` exists with a banned-words list and ≥1 real sample | 3 | F | Read samples.md |
| C4 | ≥3 real voice samples, no placeholder slots remaining | 4 | M | Count samples whose body is real (a body like `[PASTE ...]` does NOT count) |
| C5 | ≥1 real (non-`.gitkeep`) file in `context/references/` | 3 | M | List `context/references/` recursively, ignore `.gitkeep` |
| C6 | `context/strategy.md` modified within 90 days | 3 | M | Check file mtime |

### R — Reach (max 20 pts)

| # | Check | Pts | Type | How to check |
|---|-------|-----|------|-------------|
| R1 | `reach/data/intel.db` exists with an `emails` table | 4 | F | Check file + table |
| R2 | `reach/auth/token.json` present with both `gmail.readonly` and `gmail.compose` scopes | 4 | F | Read token.json `scopes` |
| R3 | `emails` table has ≥1 record | 4 | F | `SELECT COUNT(*) FROM emails` |
| R4 | emails collected within last 2 days (inbox kept fresh) | 5 | M | `SELECT MAX(collected_at) FROM emails` |
| R5 | emails collected within last 7 days | 3 | M | same query, 7-day window |

### A — Actions (max 20 pts)

| # | Check | Pts | Type | How to check |
|---|-------|-----|------|-------------|
| A1 | Core workflow skills present: `analyze.md`, `plan.md`, `build.md` | 4 | F | Check files in `.claude/commands/` |
| A2 | `/triage` skill present and time-saved logging wired (`actions/triage/runlog.py` + `triage_runs` table) | 4 | F | Check `.claude/commands/triage.md`, runlog.py, table |
| A3 | triage test suite passes | 4 | F | Run `python -X utf8 -m pytest tests/triage/ -q` → all pass |
| A4 | triage has produced ≥1 real draft end-to-end | 5 | M | `SELECT COUNT(*) FROM triage_actions WHERE action='drafted'` ≥ 1 |
| A5 | ≥5 cumulative drafts produced | 3 | M | same query ≥ 5 |

### F — Flow (max 20 pts)

> This project's real cadence is the triage habit + GTD — not the template's daily brief, scheduler, or Telegram bot. Those are deliberately not built and are NOT scored.

| # | Check | Pts | Type | How to check |
|---|-------|-----|------|-------------|
| F1 | All 8 GTD files present in `flow/gtd/` | 4 | F | inbox, projects, next-actions, waiting-for, someday-maybe, areas, dashboard, review-checklist |
| F2 | triage is a repeatable process (refresh + draft wired: `actions/triage/emails.py`, `gmail_draft.py`) | 4 | F | Check files exist |
| F3 | `/triage` run within last 2 days | 5 | M | `SELECT MAX(run_date) FROM triage_runs` |
| F4 | `/triage` run on ≥3 distinct days in last 7 (the daily-habit proof) | 4 | M | `SELECT COUNT(DISTINCT run_date) FROM triage_runs WHERE run_date >= <today-6d>` ≥ 3 |
| F5 | GTD inbox processed (at/near zero — only the template header remains, no captured items) | 3 | M | Read `flow/gtd/inbox.md` |

### T — Tuning (max 20 pts)

| # | Check | Pts | Type | How to check |
|---|-------|-----|------|-------------|
| T1 | `tune.md` and `audit.md` skills present | 4 | F | Check files |
| T2 | `tuning/changelog.md` has ≥2 entries | 4 | F | Count `## ` date sections |
| T3 | ≥1 prior audit exists in `tuning/audits/` (baseline set) | 4 | M | Count non-`.gitkeep` files |
| T4 | ≥2 audits exist in `tuning/audits/` (a visible trend) | 4 | M | same count ≥ 2 |
| T5 | changelog grew within last 14 days OR ≥1 completed plan (`Status: Complete`) in `tuning/plans/` | 4 | M | Check changelog latest date / plans |

## Step 2: Calculate Scores

Tally points per layer. Per-layer grade (out of 20):
- 18–20: A · 15–17: B · 11–14: C · 7–10: D · 0–6: F

Overall grade (out of 100):
- 90–100: A · 75–89: B · 60–74: C · 40–59: D · 0–39: F

## Step 3: Produce the Report

```markdown
# CRAFT Audit — [date]

> Rubric v2 (project-adapted). Score History below compares v2 runs only; the v1 pre-adaptation baseline is noted separately and not comparable.

### Overall Score: [total]/100 ([overall grade])

| Layer | Score | Max | Grade |
|-------|-------|-----|-------|
| C — Context | [c] | 20 | [grade] |
| R — Reach | [r] | 20 | [grade] |
| A — Actions | [a] | 20 | [grade] |
| F — Flow | [f] | 20 | [grade] |
| T — Tuning | [t] | 20 | [grade] |
| **Total** | **[total]** | **100** | **[overall]** |

### Check-by-check
[List each check: ✓/✗, points, and a one-line note. Mark F or M.]

### Top Gaps (prioritized by impact on the Q2 strategy)
[Lead with the gaps that sit on priority work — real drafts (A4/A5), daily-habit (F4), audit trend (T4), context depth (C4/C5). For each: what's missing → specific fix. Maturity gaps that ARE the strategy outrank foundation trivia.]

### What's Working
- [Layer]: [brief note]

### Score History (v2 rubric)
[today]: [score]/100
[prior v2 runs, if any]
(v1 pre-adaptation baseline, not comparable: 2026-05-29 = 63/100)

### Recommended Next Action
[Single most impactful thing — should almost always be a Maturity check on the critical path. End with the specific command or action.]
```

## Step 4: Save the Report

Save to: `tuning/audits/[YYYY-MM-DD]-audit.md`.
- If a file already exists for today (e.g. a prior-rubric baseline), do NOT overwrite it — save as `[YYYY-MM-DD]-audit-v2.md` so the earlier baseline is preserved.

Append to `tuning/changelog.md`:
```
## [date]
- Audit run (v2): [score]/100. Top gap: [layer] — [the maturity check to move next].
```

Print: "Audit saved to tuning/audits/[filename].md"

## Behavior Rules

- Be honest. Zero points means zero — no partial credit for half-done items.
- Prioritize the gap list by impact on the current Q2 strategy, not by raw score. A maturity check on the critical path (producing real drafts, the daily-triage habit) outranks a missing foundation file.
- Do NOT reward or recommend building the template features this project cut (Telegram bot, daily brief, scheduler, business-metrics collectors). They are out of scope by design.
- Always end with exactly one recommended next action — ideally the cheapest maturity point on the critical path.
