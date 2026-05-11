---
name: build
description: Execute a plan from tuning/plans/ step by step. Marks each step complete as it goes. Resumes from the first incomplete step if interrupted. Usage: /build [path-to-plan-file]
user_invocable: true
trigger: /build
version: 1.0.0
---

# /build — Execute a Plan

## Step 1: Read the Plan

Read the plan file at the path the user specified.

If the file doesn't exist: "Plan file not found at [path]. Run `/plan [topic]` to create one."

If `Status: Complete`: "This plan is already marked complete. Nothing to do."

## Step 2: Check Dependencies

Read the Dependencies section. For each unchecked dependency:
- Warn the user: "Dependency not confirmed: [dependency]"
- Ask: "Do you want to continue anyway?"
- If they say yes, note it and proceed. If no, stop.

## Step 3: Find Starting Point

Find the first unchecked step (`- [ ]`).

If some steps are already checked, print:
```
Resuming from Step [N].
Previously completed: [list of checked steps]
```

If all steps are unchecked, print: "Starting build: [Plan Title]"

## Step 4: Execute Each Step

For each unchecked step, in order:

**Print the step:**
```
--- Step [N]: [Step description] ---
```

**Execute based on step type:**

- **File creation / editing:** Use the Write or Edit tool to create or modify the file. Show what was created/changed.
- **Shell command:** Print the exact command in a code block. Ask the user to run it and confirm the output. Wait for confirmation before moving on.
- **Configuration:** Edit `.env` or `CRAFT.md` using the Edit tool. Show the change.
- **Verification:** Run the check or ask the user to run it. Confirm pass/fail.

**After each step:**
- Mark it complete in the plan file: change `- [ ]` to `- [x]`
- Print: `✅ Step [N] complete.`
- Continue to the next step.

## Step 5: Run Validation

After all steps are complete, run the validation from the plan's Validation section.

Report clearly: "✅ Validation passed." or "❌ Validation failed: [what went wrong]"

If validation fails, do not mark the plan as complete. Explain what to fix.

## Step 6: Mark Complete and Finish

Update the plan file: change `Status: Draft` or `Status: In Progress` to `Status: Complete`.

Print:
```
✅ Build complete: [Plan Title]

What was built: [brief list of what was created/changed]
Validation: passed

Run `/push` to save your progress to GitHub.
```

## Build Rules

- Never skip a step without explicit user permission.
- Never modify files not mentioned in the plan without asking first.
- If something unexpected comes up mid-build, stop and ask — don't improvise.
- Keep the plan file updated as you go — it's the live record of progress.
- If a step fails, stop, explain the error clearly, and ask the user how to proceed.
