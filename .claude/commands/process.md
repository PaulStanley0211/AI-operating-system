---
name: process
description: Empty the GTD inbox to zero. Walks each item through the decision tree and routes to next-actions, projects, waiting-for, someday-maybe, or trash. Run when flow/gtd/inbox.md has items.
user_invocable: true
trigger: /process
version: 1.0.0
---

# /process — Empty the Inbox

## Step 1: Check the Inbox

Read `flow/gtd/inbox.md`.

Count the items. If inbox is empty: "Inbox is already at zero. Nothing to process." Stop.

If more than 10 items: "Found [N] items. Processing in batches of 10. Starting with the first batch."

## Step 2: Process Each Item

Work through items one at a time. For each item, run the decision tree:

---

### The Decision Tree

**Question 1: Is it actionable?**

→ **NO** — pick one:
  - **Trash** — delete from inbox, no record needed
  - **Someday/Maybe** — add to `flow/gtd/someday-maybe.md`
  - **Reference** — useful info; file it (ask where)

→ **YES** — continue to Question 2

**Question 2: What is the next physical action?**

The next action must be a specific, visible physical activity. Not "deal with X" — something like "call Sarah," "draft the proposal," "read the pricing page."

Suggest the next action based on the item. The user confirms or corrects.

**Question 3: Does it take less than 2 minutes?**

→ **YES** — tell the user to do it right now. Log it as done. Move on.

→ **NO** — continue to Question 4

**Question 4: Who does it?**

→ **Someone else** — add to `flow/gtd/waiting-for.md`:
  ```
  | [Item description] | [Owner/Person] | [Date sent] | [Expected by] |
  ```

→ **Me** — continue to Question 5

**Question 5: Is it a project?**

A project is anything that requires more than one action step to complete.

→ **YES** — add to `flow/gtd/projects.md` under the right area, with an outcome. Extract one next action → add to `flow/gtd/next-actions.md`.

→ **NO** — add directly to `flow/gtd/next-actions.md` with the right context tag.

---

## Step 3: Context Tags

When adding to next-actions.md, always assign a context tag:

| Tag | When to use |
|-----|-------------|
| `@me` | Only I can do this, requires focus |
| `@claude` | Can be delegated to Claude in a session |
| `@calls` | Requires a phone call |
| `@errands` | Requires being somewhere physically |
| `@waiting` | Waiting on someone else (also add to waiting-for.md) |

If none fit, use `@me` as the default.

## Step 4: File Edits

After each item is routed, immediately:
1. **Remove** the item from `flow/gtd/inbox.md`
2. **Add** it to the appropriate destination file

Show each edit before making it. Do not make silent changes.

## Step 5: Batch Handling

After every 10 items, print a mid-point summary and ask: "Continue with the next [N] items?"

## Step 6: Final Summary

After all items are processed:

```
Inbox cleared. Here's where everything went:
- [X] added to next-actions
- [Y] added to projects
- [Z] added to waiting-for
- [W] sent to someday-maybe
- [V] trashed

Running dashboard refresh...
```

Run `python flow/refresh_dashboard.py` to update the dashboard.

## Interaction Style

- Be efficient. For obvious items, suggest the routing and ask for a quick confirm — don't make the user describe everything from scratch.
- Keep moving. Processing 10 items should take 5–8 minutes.
- If an item is genuinely ambiguous, ask one focused question, then route it.
