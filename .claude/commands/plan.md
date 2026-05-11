---
name: plan
description: Create a structured implementation plan before making changes. Saves to tuning/plans/ with a dated filename. Usage: /plan [what to build or do]
user_invocable: true
trigger: /plan
version: 1.0.0
---

# /plan — Create an Implementation Plan

## Step 1: Read Context

Read:
- `CRAFT.md` — know what layer this touches and what already exists
- Scan `tuning/plans/` for any existing plans on the same topic. If one exists, show it and ask: "There's an existing plan on this topic — update it, or create a new one?"

## Step 2: Parse and Clarify

Extract the topic from the user's command.

If the request is ambiguous, ask one question to clarify scope before drafting. Example:
- `/plan email automation` → "Do you mean the email-triage skill, or a full scheduled pipeline?"

If clear enough, proceed without asking.

## Step 3: Draft the Plan

Produce a plan in this exact format:

```markdown
# Plan: [Title]
<!-- v1.0.0 -->

> Created: [YYYY-MM-DD]
> Status: Draft
> CRAFT Layer: [C / R / A / F / T / INFRA]

## Goal
[One sentence: what will be true when this is done?]

## Context
[2–3 sentences: why are we doing this? What problem does it solve? What triggered it?]

## Scope

**Included:**
- [What this plan covers]

**Excluded:**
- [What this plan explicitly does NOT cover]

## Dependencies

- [ ] [What must exist or be done before this can start — check the box if already satisfied]

## Steps

- [ ] **Step 1:** [Specific, completable action]
- [ ] **Step 2:** [Specific, completable action]
- [ ] **Step 3:** [...]

## Validation

[How do we know it worked? What's the acceptance test? Be specific — "run X and see Y output."]

## Estimated Effort

[Quick (< 1 hour) / Half-day / Full day / Multi-day]

## Notes

[Any caveats, open questions, or decisions made during planning. Leave blank if none.]
```

## Step 4: Review Before Saving

Present the full plan in the chat. Ask:
"Does this look right? Any changes before I save it?"

Do not save until the user confirms.

## Step 5: Save

Save the plan to:
```
tuning/plans/[YYYY-MM-DD]-[kebab-case-title].md
```

Print: "Plan saved. Run `/build tuning/plans/[filename].md` when ready."

## Planning Rules

- Steps must be atomic — each one is a single, completable action
- Include a validation step for anything non-trivial
- If the plan touches something that doesn't exist yet, note it as a dependency
- Don't over-engineer. A 3-step plan is fine if the task is simple.
- The plan must be readable cold — someone else should be able to execute it from the plan file alone.
