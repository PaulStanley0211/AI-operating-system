# AIOS — AI Operating System

> Built with the **CRAFT Framework**. Free to use, fork, and build on.
> Created by [Tommy Chryst](https://youtube.com/@tommychryst) | [@tommychryst](https://youtube.com/@tommychryst)

---

## What This Is

A complete starter kit for building your own AIOS (AI Operating System) using the CRAFT framework. Clone this repo, fill in your context, and start building layer by layer.

**CRAFT** = Context → Reach → Actions → Flow → Tuning

Five layers. Built in order. Each one independently valuable.

---

## Quick Start

**Prerequisites:** Git, Python 3.10+, Claude Code (VS Code extension or CLI)

```bash
# 1. Clone the repo
git clone https://github.com/TommyChryst/AIOS.git your-aios
cd your-aios

# 2. Set up Python environment
python -m venv .venv
.venv/Scripts/activate        # Windows
# source .venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your secrets
cp .env.example .env
# Edit .env and fill in your API keys

# 5. Fill in your context
# Open CRAFT.md and fill in every [FILL IN] section
# Then open context/identity.md, context/business.md, etc.

# 6. Open in Claude Code and run /start
```

---

## What's Included

| Component | What it does |
|-----------|-------------|
| `CRAFT.md` | Master context file — fill this in first |
| `context/` | Identity, business, team, strategy, voice templates |
| `reach/collectors/` | Data collection scripts (YouTube, Stripe, Gmail, Fireflies) |
| `.claude/commands/` | 12 pre-built skills: /start, /pulse, /audit, /tune, and more |
| `flow/brief/` | Coffee Debrief pipeline — daily brief → Telegram |
| `flow/bot/` | Telegram bot for mobile access |
| `flow/gtd/` | GTD task management system |
| `tuning/` | Audit reports, plans, changelog |

---

## The Six Nodes

Install these in order. Each adds a new capability layer.

| # | Node | Layer | What you get |
|---|------|-------|-------------|
| 0 | Vault Node | INFRA | Workspace structure, git, GitHub |
| 1 | Context Node | C | AI knows who you are |
| 2 | Intelligence Node | R | Live data → daily brief |
| 3 | Coffee Debrief Node | A | Brief delivered to Telegram every morning |
| 4 | Mobile Node | F | Full access from your phone |
| 5 | Productivity Node | F | GTD task management |

See `node-installs/` for guided installers.

---

## Watch the Course

This repo accompanies the full CRAFT course on YouTube.
→ [Watch it here](https://youtube.com/@tommychryst)

---

## License

MIT — use it, fork it, sell setups built on it. Attribution appreciated but not required.
