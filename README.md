# AIOS — AI Operating System

> Built on the CRAFT Framework. Free to use, free to build on.
> Created by [Tommy Chryst](https://youtube.com/@tommychryst)

---

## What This Is

AIOS is a free, open-source starter kit for building your own AI Operating System using Claude Code.

The idea is simple: instead of starting every AI conversation from scratch, you build a workspace that Claude already understands. It knows your business, watches your numbers, reads your emails and meetings, and helps you stay on top of everything — automatically.

You build it in layers. Each layer makes Claude more useful. And every layer you add is yours to keep.

---

## How It Works

Your AIOS lives in a folder on your computer. Inside that folder are files that Claude reads at the start of every session — who you are, what your business does, what you're focused on right now, and what tools are available. The better those files are, the smarter Claude gets.

The CRAFT Framework is how those layers are organized:

```
C — Context     → Claude knows your business
R — Reach       → Claude sees your live data
A — Actions     → Claude synthesizes it into a daily brief
F — Flow        → Claude manages tasks and talks to you from your phone
T — Tuning      → Claude gets better over time
```

You don't have to build all five layers. Every layer you complete is independently useful from the moment it's done.

---

## How to Get Started

Everything installs through Claude Code. Clone this repo, open the folder in Claude Code, and run:

```
/install core-node-installs/01-vault-node
```

Claude will walk you through setup step by step — asking questions about your business, your tools, and what you want to track. You don't need to figure anything out in advance. Just answer the questions and Claude builds it.

**Install the nodes in order:**

| # | Node | What you get |
|---|------|-------------|
| 01 | [Vault Node](core-node-installs/01-vault-node/) | Your workspace structure and foundation |
| 02 | [Context Node](core-node-installs/02-context-node/) | Claude learns your business inside and out |
| 03 | [Intelligence Node](core-node-installs/03-intelligence-node/) | Claude starts seeing your live business data |
| 04 | [Coffee Debrief Node](core-node-installs/04-coffee-debrief-node/) | A morning brief delivered to your phone every day |
| 05 | [Mobile Node](core-node-installs/05-mobile-node/) | Full access to your AI from Telegram |
| 06 | [Productivity Node](core-node-installs/06-productivity-node/) | Task management and weekly reviews |

You don't have to install all of them. Stop at any point — what you've built is already working.

---

## What You Can Do Once It's Running

Once your AIOS is set up, you have a set of commands available in Claude Code at all times:

| Command | What it does |
|---------|-------------|
| `/start` | Start your session — Claude loads your context and shows you what's happening |
| `/pulse` | Get a live snapshot of your business numbers |
| `/process` | Clear your task inbox — Claude routes everything to the right place |
| `/review` | Guided weekly review of everything on your plate |
| `/email-triage` | Claude reads your inbox and drafts replies in your voice |
| `/audit` | Score how complete and healthy your AIOS is |
| `/tune` | Get recommendations for what to improve or automate next |
| `/install` | Install a node |

---

## What You'll Need to Do Yourself

Claude does the heavy lifting, but there are a few things only you can do:

- **Connect your accounts** — YouTube, Stripe, Gmail, Telegram. Claude tells you exactly what to get and where to find it, but you'll need to log in and grab the keys yourself.
- **Fill in your context** — Claude will ask you questions during setup, but the better you answer them, the better your AIOS will be. Be honest and specific.
- **Show up weekly** — The task system only works if you review it. Thirty minutes a week keeps everything running.

That's it. Everything else Claude handles.

---

## Watch the Course

This repo accompanies the full CRAFT course on YouTube.
→ [Watch it here](https://youtube.com/@tommychryst)

---

## License

MIT — use it, fork it, build on it.
