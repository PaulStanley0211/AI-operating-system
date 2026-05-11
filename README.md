# AIOS — AI Operating System

> Built on the CRAFT Framework. Give your AI a brain, eyes, a voice, and a task list.
> Created by [Tommy Chryst](https://youtube.com/@tommychryst) | Part of the [AAA Accelerator](https://aaaaccelerator.com)

---

## What This Is

AIOS is a free, open-source operating layer that turns Claude Code into a full business intelligence system. It gives your AI:

- **Context** — it knows your business, your voice, your priorities
- **Data** — it watches your metrics every day, automatically
- **Intelligence** — it reads your emails and meetings, synthesizes them into a morning brief
- **Automation** — it captures tasks, manages your to-do list, and helps you run weekly reviews
- **A phone interface** — full access to your AI from Telegram

Everything runs locally on your machine. Your data stays yours.

---

## What It Does

Once fully installed, AIOS gives you:

| Capability | What you get |
|-----------|-------------|
| **Session context** | Every Claude session starts knowing who you are, what your business is, and what you're working on |
| **Live metrics** | YouTube subscribers, Stripe revenue, email counts — collected daily into a local database |
| **Daily brief** | A structured morning intelligence report delivered to your phone by 7 AM |
| **Email digest** | Noise-filtered Gmail and Outlook emails surfaced in every brief |
| **Meeting summaries** | Fireflies transcripts ingested, searchable, included in your brief |
| **Telegram bot** | Ask business questions, query metrics, capture tasks — from your phone |
| **GTD task system** | Capture inbox, process actions, manage projects, run weekly reviews |
| **Slash commands** | `/start`, `/pulse`, `/process`, `/review`, `/audit`, `/tune` and more |

---

## How to Install

AIOS installs in layers called **nodes**. Each node is independent — install what you need, skip what you don't.

**Prerequisites:**
- [Claude Code](https://claude.ai/code) installed
- Python 3.10+ with a virtual environment (`python -m venv .venv`)
- Git

**Clone the repo:**
```bash
git clone https://github.com/TommyChryst/AIOS.git your-aios
cd your-aios

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

**Installation order (recommended):**

```
1. Vault Node        → creates the workspace structure
2. Context Node      → teaches the AI who you are
3. Intelligence Node → connects your data sources
4. Coffee Debrief Node → generates your morning brief
5. Mobile Node       → adds Telegram access from your phone
6. Productivity Node → adds GTD task management
```

**To install any node, open Claude Code and run:**
```
/install node-installs/vault-node
```

Claude will ask you setup questions tailored to your business, then build everything configured for your specific answers. You don't need to install all nodes — stop at any layer that gives you what you need.

---

## How to Know It's Working

After all nodes are installed, run this in Claude Code:
```
/audit
```

This scores your AIOS across all 5 layers (0–100). A fully working system scores 80+.

**Day-to-day signals:**
- `/start` gives you a session summary with your actual business metrics
- You receive a morning brief in Telegram by 7 AM
- `/pulse` returns live numbers from your connected data sources
- `/process` clears your task inbox

---

## What to Expect

**Week 1** — 2–3 hours of setup across nodes and API connections. By the end, you have a working daily brief and Claude knows your business.

**Week 2** — The system builds a data history. You start seeing trends. The morning brief gets more useful.

**Month 1** — You're running weekly GTD reviews, triaging email faster, and delegating routine thinking to Claude inside sessions.

**Ongoing** — Run `/tune` monthly for improvement recommendations. Run `/audit` quarterly to measure AIOS health and find gaps.

---

## What You Have to Do Yourself

AIOS automates a lot but requires human setup for anything that touches external accounts:

| Task | Frequency |
|------|-----------|
| Create API keys (YouTube, Stripe, Telegram, etc.) | One-time per source |
| Run Gmail/Outlook OAuth authorization | One-time per account |
| Fill in CRAFT.md (your business context) | One-time, update as things change |
| Schedule the daily Windows Task or cron job | One-time |
| Review your GTD system weekly | Weekly (30–60 min) |
| Update `context/strategy.md` when priorities shift | Monthly |

The system is only as useful as what you put into it. CRAFT.md is your foundation — keep it current and honest.

---

## The CRAFT Framework

```
C — Context     → CRAFT.md, identity, business, voice, strategy
R — Reach       → Data collectors, SQLite database, metrics.md
A — Actions     → Daily brief, email triage, meeting intelligence
F — Flow        → GTD task management, Telegram bot, weekly review
T — Tuning      → Audit, tune, changelog, brief archive
```

Each letter is a layer. Each layer is built by one or more nodes. You build in order — but each layer is independently useful the moment it's done.

---

## Available Nodes

| Node | Layer | What it adds |
|------|-------|-------------|
| [Vault Node](node-installs/vault-node/) | Infra | Workspace structure, CRAFT.md, Python environment |
| [Context Node](node-installs/context-node/) | C | Identity, business context, voice, AI conversation import |
| [Intelligence Node](node-installs/intelligence-node/) | R | Data collectors, SQLite database, daily metrics |
| [Coffee Debrief Node](node-installs/coffee-debrief-node/) | A | Daily brief generation and Telegram delivery |
| [Mobile Node](node-installs/mobile-node/) | F | Telegram bot — full AIOS access from your phone |
| [Productivity Node](node-installs/productivity-node/) | F | GTD task system, inbox, projects, weekly review |

---

## Available Skills (Slash Commands)

Skills are installed automatically — no setup required. Open Claude Code and start using them.

| Command | What it does |
|---------|-------------|
| `/start` | Load full context, show metrics, begin session |
| `/pulse` | Live snapshot of key business metrics |
| `/process` | Process GTD inbox to zero |
| `/review` | Guided weekly GTD review |
| `/email-triage` | Classify and draft replies for your inbox |
| `/audit` | Score your AIOS across all 5 layers |
| `/tune` | Get prioritized improvement recommendations |
| `/create-plan` | Plan a new feature or change before building |
| `/implement` | Execute a plan step by step |
| `/install` | Install a node |
| `/share` | Package a system to share with others |
| `/prime` | Re-initialize session context |

---

## Watch the Course

This repo accompanies the full CRAFT course on YouTube.
→ [Watch it here](https://youtube.com/@tommychryst)

---

## License

MIT — use it, fork it, build on it. Attribution appreciated but not required.
