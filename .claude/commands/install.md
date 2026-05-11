---
name: install
description: Install a CRAFT node into this workspace. Reads the node's INSTALL.md, asks setup questions upfront, then walks through guided setup step by step. Usage: /install [path-to-node-folder]
user_invocable: true
trigger: /install
version: 1.1.0
---

# /install — Node Installation

## Step 1: Locate and Read the Node

Parse the path from the user's command (e.g., `/install core-node-installs/03-intelligence-node`).

Read the following files from that folder:
- `INSTALL.md` — required. If missing, stop and say: "This folder doesn't have an INSTALL.md. CRAFT nodes need an INSTALL.md to be installed with /install."
- `README.md` — optional, read if present for context.

## Step 2: Show What's About to Be Installed

Print a brief summary:
```
📦 [Node Name] — v[version]
[One-line description of what the node does]

This will install:
- [list key files/folders]
- [list .env variables to be added]
- [list CRAFT.md sections to be updated]
```

Ask: "Ready to begin setup? I'll ask a few quick questions first."

## Step 3: Run Setup Questions (BEFORE doing anything)

This is the most important step. Read the `## Setup Questions` section of INSTALL.md.

Ask every question in that section **before touching any files or collecting any API keys**. Ask them one at a time, conversationally. Wait for each answer before asking the next.

After collecting all answers:
- Print a short summary: "Based on your answers, here's what we'll set up: [list]"
- List anything being skipped and why: "Skipping: [X] — you said [reason]"
- Ask: "Does that look right? Ready to proceed?"

**Use the answers throughout the rest of the install to:**
- Skip steps that don't apply to this person's setup
- Pre-fill configuration values where possible
- Adjust which .env variables to collect
- Customize any template files with their specific answers (business name, areas, etc.)

The goal is that by the end of setup, the installed node feels configured for *this* person — not like a generic template they'll have to fill in later.

## Step 4: Walk Through Prerequisites

Read the Prerequisites section. For each item:
- Check if it's likely already satisfied based on context and prior answers
- Skip prerequisites that don't apply based on Setup Questions answers
- For accounts or API keys: tell the user exactly where to get them
- Pause if any prerequisite is clearly not met. Don't continue until it's resolved.

## Step 5: Collect .env Variables

Only collect variables that are relevant based on the Setup Questions answers. Skip variables for services the user said they don't use.

For each relevant variable:
- Ask the user to provide the value (or confirm they've already added it)
- Once confirmed, add it to `.env` using the Edit tool
- Never print the value back — just confirm it was added

## Step 6: Create and Customize Files

For each file in the `Files Installed` section:
- Create it using the Write tool
- Where possible, pre-fill it with answers from the Setup Questions (business name, areas of responsibility, preferred tools, etc.)
- Don't leave `[FILL IN]` markers for things the user already told you — fill them in now
- Confirm each file after creation

## Step 7: Update CRAFT.md

If INSTALL.md specifies CRAFT.md additions, make those edits now. Show the user what was added.

## Step 8: Run Setup Steps

For each step in `Setup Steps`:
- Skip steps that don't apply based on Setup Questions answers
- If it's a shell command: print it in a code block, ask the user to run it, wait for confirmation
- If it's a file edit: do it directly
- If it requires user input: ask for it

## Step 9: Validation

Run the validation check from the `Validation` section.
- Print the command and ask the user to run it
- Confirm expected output
- Report pass/fail clearly

## Step 10: Log and Finish

1. Add an entry to `tuning/changelog.md`:
   ```
   ## [today's date]
   - Installed: [Node Name] v[version]
   - Configuration: [brief note on what was enabled/skipped based on their answers]
   ```
2. Print completion summary:
   ```
   ✅ [Node Name] installed successfully.

   What was installed: [brief list]
   Configured for: [their specific setup based on answers]
   .env variables added: [key names only, not values]
   Skipped: [anything not installed and why]

   Next: [what to do now, from INSTALL.md]
   ```

## Error Handling

- If a step fails, stop and explain the error clearly. Do not skip ahead.
- If the user says "skip" on a non-critical step, note it and continue.
- If a file already exists at a target path, warn before overwriting.
- If a Setup Question answer conflicts with a prerequisite, flag it before proceeding.
