---
name: install
description: Install a CRAFT node into this workspace. Reads the node's INSTALL.md and walks through guided setup step by step. Usage: /install [path-to-node-folder]
user_invocable: true
trigger: /install
version: 1.0.0
---

# /install — Node Installation

## Step 1: Locate and Read the Node

Parse the path from the user's command (e.g., `/install node-installs/intelligence-node`).

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

Ask: "Ready to install? (yes/no)"

## Step 3: Walk Through Prerequisites

Read the Prerequisites section of INSTALL.md. For each item:
- Check if it's likely satisfied (e.g., if it requires Python, it's probably already installed)
- For API keys or accounts: tell the user where to get them before proceeding
- Pause if any prerequisite is clearly not met. Don't continue until it's resolved.

## Step 4: Collect .env Variables

For each variable listed in the INSTALL.md `.env Variables Required` section:
- Ask the user to provide the value (or confirm they've already added it)
- Once confirmed, add the variable to `.env` using the Edit tool
- Never print the value back — just confirm it was added

## Step 5: Create Files

For each file listed in the INSTALL.md `Files Installed` section:
- Create the file at the specified path using the Write tool
- Use the node's template content if provided in INSTALL.md
- Confirm each file after creation

## Step 6: Update CRAFT.md

If INSTALL.md specifies CRAFT.md additions, make those edits now using the Edit tool. Show the user what was added.

## Step 7: Run Setup Steps

For each step in the INSTALL.md `Setup Steps` section:
- If it's a shell command: print it in a code block, ask the user to run it, wait for confirmation
- If it's a file edit: do it directly
- If it requires user input (API key, config value): ask for it

## Step 8: Validation

Run the validation check from the INSTALL.md `Validation` section.
- If it's a command: print it and ask the user to run it, then confirm the expected output
- Report pass/fail clearly

## Step 9: Log and Finish

1. Add an entry to `tuning/changelog.md`:
   ```
   ## [today's date]
   - Installed: [Node Name] v[version]
   ```
2. Print completion summary:
   ```
   ✅ [Node Name] installed successfully.
   
   What was installed: [brief list]
   .env variables added: [key names only, not values]
   
   Next: [what to do now, from INSTALL.md]
   ```

## Error Handling

- If a step fails, stop and explain the error clearly. Do not skip ahead.
- If the user says "skip" on a non-critical step, note it and continue.
- If a file already exists at a target path, warn before overwriting.
