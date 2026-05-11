---
name: push
description: Commit all workspace changes to git and push to GitHub. Auto-generates a commit message from what changed. Usage: /push or /push "custom message"
user_invocable: true
trigger: /push
version: 1.0.0
---

# /push — Commit and Push to GitHub

## Step 1: Check Status

Run: `git status`

If nothing is changed, print: "Nothing to commit. Workspace is up to date." and stop.

## Step 2: Safety Check

Before staging anything, verify these files are NOT in the changed list:
- `.env`
- `reach/data/*.db`
- Any file named `*.key`, `*.pem`, `*.secret`, `token.json`, `msal_token_cache.json`

If any of these appear in `git status`:
- Do NOT proceed with the push
- Explain what happened and how to fix `.gitignore`
- Print the fix command: `echo "[filename]" >> .gitignore`

## Step 3: Generate Commit Message

If the user passed a message after `/push` (e.g., `/push "add email triage skill"`), use that exactly.

If no message was provided, generate one from the changed file list:
- Only `flow/gtd/` files changed → `"gtd: [brief description of changes]"`
- Only `reach/` files changed → `"reach: [brief description]"`
- Only `CRAFT.md` changed → `"context: update CRAFT.md"`
- Only `.claude/` files changed → `"skills: [brief description]"`
- Only `tuning/` files changed → `"tuning: [brief description]"`
- Mixed changes → `"workspace: [brief description of the most significant change]"`

Keep messages under 60 characters.

## Step 4: Commit and Push

Run these in sequence:
```
git add .
git commit -m "[commit message]"
git push origin HEAD
```

Show the output of each command.

## Step 5: Confirm

Print:
```
✅ Pushed.
Branch: [current branch]
Commit: [short hash] — [commit message]
```

If `push` fails due to auth:
- Check if `GITHUB_TOKEN` is in `.env`
- If not: "Add your GitHub personal access token to .env as GITHUB_TOKEN, then try again."
- If yes: "Push failed. Check that your token has 'repo' scope and the remote URL is correct."
