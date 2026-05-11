# Vault Node

> Layer: Infrastructure
> The foundation everything else is built on.

---

## What It Is

The Vault Node sets up your AIOS workspace — the folder structure, the master context file (CRAFT.md), your Python environment, and your git repository. Every other node installs into a workspace that Vault creates.

You install this first. It takes about 10 minutes.

---

## What It Does

- Creates the full folder structure for your AIOS (`context/`, `reach/`, `flow/`, `tuning/`, `outputs/`, etc.)
- Installs `CRAFT.md` — the single file that tells Claude who you are, what your business does, and how you like to work
- Installs `requirements.txt` and confirms your Python environment is ready
- Initializes a git repository so your workspace is version-controlled from day one
- Optionally pushes to a private GitHub repo so your work is backed up and accessible

---

## How to Install

Open Claude Code in the AIOS folder and run:
```
/install node-installs/vault-node
```

Claude will ask you 5 setup questions before touching anything:
1. Your name and business name
2. A one-sentence description of what your business does
3. Whether you're solo or have a team
4. Your operating system (Windows, Mac, or Linux)
5. Whether you have a GitHub account to push to

Your answers are used to pre-fill CRAFT.md and skip irrelevant steps.

---

## How to Know It's Working

After install, check these:

- [ ] `CRAFT.md` exists in the root folder and has your name/business filled in
- [ ] All expected directories exist: `context/`, `reach/`, `flow/`, `tuning/`, `outputs/`
- [ ] `.env.example` exists (copy to `.env` and start filling in keys as you go)
- [ ] `requirements.txt` is installed in your virtual environment
- [ ] `git status` shows a clean repo with an initial commit
- [ ] (Optional) `git remote -v` shows your GitHub repo

Run `/start` in Claude Code — it should greet you by name and describe your business correctly.

---

## What to Expect

The Vault Node installs quickly. Most of the work is filling in CRAFT.md after install.

CRAFT.md has sections for: About Me, The Business, Team, Strategy This Quarter, Voice, Email Profile, and Working Preferences. You don't need to fill it all in on day one — but the more complete it is, the more useful every Claude session becomes.

Leave `[FILL IN]` in any section you're not ready for. Come back to it.

---

## What You Have to Do Yourself

| Task | Notes |
|------|-------|
| Fill in `CRAFT.md` | Most important thing you'll do in this node — take your time |
| Create a GitHub repo | If you want version control + backup (recommended) |
| Copy `.env.example` to `.env` | Needed before any data sources are connected |

That's it. Vault is pure structure — no external APIs, no credentials required.

---

## Next Step

Once Vault is done:
```
/install node-installs/context-node
```
