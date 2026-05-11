---
name: tune
description: Monthly tuning session. Reviews manual task patterns, audit history, and brief signals to recommend the next automation or layer to build. Run monthly, after /audit.
user_invocable: true
trigger: /tune
version: 1.0.0
---

# /tune — Monthly Tuning Session

## Step 1: Check Recency

Look for the most recent file in `tuning/audits/`. If the latest audit is more than 14 days old, say:
"Your last audit was [N] days ago. For the best tune session, run `/audit` first, then come back."

Continue regardless of whether they run the audit.

## Step 2: Gather Evidence

Read each of the following (skip gracefully if a file/directory doesn't exist):

1. **Latest audit** from `tuning/audits/` — current score and top gaps
2. **`tuning/changelog.md`** — what has been built recently (last 60 days)
3. **Last 7 files** from `tuning/briefs/` — signals that are repeating
4. **`flow/gtd/next-actions.md`** — find all `@claude` items and note any added more than 14 days ago
5. **`flow/gtd/projects.md`** — look for projects marked "On hold" for more than 30 days
6. **`CRAFT.md`** — the Mentor Instruction section (any flags it's been surfacing)

## Step 3: Ask 3–5 Questions

Before producing recommendations, ask the user 3–5 targeted questions based on what you found. Pick the most relevant ones:

- "What task have you done manually more than 3 times in the last month?"
- "What's still taking the most of your time each week?"
- "Looking at your @claude next-actions — is there one you keep meaning to automate but haven't?"
- "Is there any data you wish the brief included that it currently doesn't?"
- "Which layer of CRAFT feels most broken or underbuilt to you right now?"
- "If you could automate one thing before next month, what would it be?"

Listen to the answers. These weight the recommendations more than any system data.

## Step 4: Identify Patterns

Cross-reference the user's answers with the evidence gathered:

- **Repeating signal:** same topic appearing in 3+ briefs → automation candidate
- **Aging @claude item:** on the list 14+ days → high-friction task worth building
- **Stalled project:** on hold 30+ days → dead weight or needs a forcing function
- **Consistent audit gap:** same layer below 10/20 in the last 2+ audits → not improving
- **User-named pain:** anything the user explicitly named in Step 3 → top priority regardless of data

## Step 5: Produce the Tune Report

```markdown
## Tune Session — [date]

### What I Found

**Repeating manual tasks:**
- [Task that appeared multiple times] (source: [briefs/next-actions/both])
- [...]

**Brief signals (last 7 briefs):**
- [Signal] — appeared [N] times, no resolution in system
- [...]

**Aging @claude items:**
- "[Item]" — added [N] days ago, not yet executed

**Audit trend:**
[date]: [score]/100
[date]: [score]/100
Weakest layer: [layer] ([score]/20)

---

### Recommendations (ranked by impact)

1. **[Short title]** ([layer] gap / [type of issue])
   [1–2 sentence explanation of why this is the top priority]
   → `/plan [specific topic]`

2. **[Short title]**
   [Explanation]
   → `/plan [specific topic]`

3. **[Short title if 3 strong candidates exist]**
   [Explanation]
   → `/plan [specific topic]`

---

### This Month's Focus
[One sentence on which recommendation to start with and why]
Run: `/plan [specific topic from #1]`
```

## Step 6: Close

Ask: "Want to run `/plan [topic]` now to get started on #1?"

If yes: kick off the `/plan` skill immediately.

## Behavior Rules

- Maximum 4 recommendations. Don't produce a dump — produce a ranked list.
- #1 must be genuinely the highest-impact action, not the easiest. Weight by time saved × frequency.
- The user's felt pain (Step 3 answers) outweighs system data in prioritization.
- Always end with a specific `/plan` command, not just a description.
- If nothing is broken and the system is healthy, say so: "Your system is in good shape. The one thing worth doing this month is [X]."
