# Vault Node — Install Guide
<!-- v1.1.0 -->

> Layer: INFRA | Must be installed first.
> Installs the workspace structure, initializes git, and connects to GitHub.

---

## What This Node Does

Creates the CRAFT folder structure, sets up git version control, and connects the workspace to a private GitHub repository. After this node, the workspace is backed up and every change can be committed with `/push`.

This node ships with the base repo — if you cloned this repo, the Vault Node is already installed. Follow these steps to complete the setup.

---

## Setup Questions

Ask these before doing anything. Use the answers to configure the install.

1. **Are you working solo, or do you have a team?**
   *(Solo = simplify team.md. Team = set up proper roles section)*

2. **Do you already have a GitHub account and a personal access token?**
   *(Yes = skip account setup. No = walk through creating both before proceeding)*

Identity and business questions come in the Context Node. Platform and deployment questions come in the Mobile Node.

---

## Prerequisites

- [ ] Git installed (`git --version` to verify)
- [ ] GitHub account created (free tier is fine)
- [ ] GitHub personal access token with `repo` scope ([create one here](https://github.com/settings/tokens))
- [ ] Claude Code installed (VS Code extension or CLI)

---

## .env Variables Required

| Variable | Description | Where to get it |
|----------|-------------|----------------|
| `GITHUB_TOKEN` | Personal access token for git push | github.com/settings/tokens → New token → `repo` scope |

---

## Files Installed

All files are already present if you cloned this repo. Verify these exist:

- `CLAUDE.md` — master context file
- `.gitignore` — secrets and database files excluded
- `.env.example` — template for your secrets
- `tuning/changelog.md` — version history
- All `context/`, `reach/`, `flow/`, `tuning/` folders

---

## Setup Steps

1. **Create your `.env` file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your GitHub token to `.env`:**
   Open `.env` and set: `GITHUB_TOKEN=your_token_here`

3. **Verify git is initialized:**
   ```bash
   git status
   ```
   If you see "not a git repository", run: `git init`

4. **Set your GitHub remote** (if not already set):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   ```
   Verify: `git remote -v`

5. **Open Claude Code:**
   Open the workspace folder in VS Code with Claude Code extension, or run `claude` in the terminal from this directory.

6. **Run `/start`:**
   Type `/start` in Claude Code. It should produce a brief session summary — context will be sparse until the Context Node is installed, which is fine.

---

## Validation

Run `/start` in Claude Code. If it responds without errors and acknowledges the workspace, the Vault Node is working.

---

## Next Steps

Install the Context Node to teach the AI who you are, what your business does, and how to sound like you:
```
/install core-node-installs/02-context-node
```

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.1.0 | 2026-05-12 | Removed OS question (belongs in Mobile Node) |
| 1.0.0 | Initial release | Base vault structure |
