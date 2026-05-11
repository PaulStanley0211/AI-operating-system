# 06 — Productivity Node

> Get everything out of your head and into a system Claude can help you manage.

---

## What It Is

The Productivity Node installs a task management system built around the GTD method (Getting Things Done). It gives Claude a structured place to hold everything you're working on — not just a to-do list, but a full system: a capture inbox, active projects, delegated items, future ideas, and a weekly review you actually look forward to running.

If you've been keeping things in your head, scattered across apps, or just feeling like you're constantly forgetting something — this is the fix.

---

## What It Does

This node creates your task system inside your workspace. Here's what it sets up:

**Your inbox** — everything gets captured here first. Voice notes from Telegram, things that pop into your head, emails you need to act on. Dump it all in. You sort it later.

**Your projects** — active things you're working toward, each with a clear next step and what "done" looks like.

**Your next actions** — the specific things you can actually do right now, organized by context. @me, @calls, @errands, and a dedicated @claude list for things you want Claude to handle.

**Waiting-for** — things you've delegated or are waiting on. So nothing slips through because you forgot you were waiting on someone.

**Someday-maybe** — ideas and commitments you want to revisit in the future but aren't ready to act on yet.

**Weekly review** — a guided 4-phase review you run with Claude. It takes about 30–60 minutes and keeps the whole system healthy.

---

## What Happens During Install

Open Claude Code and run:
```
/install core-node-installs/06-productivity-node
```

Before building anything, Claude asks you:

- What areas of your life and work you're responsible for
- What 3–5 real projects you're actively working on right now
- Anything that's been sitting in your head that you've been meaning to do
- What day and time works best for your weekly review

Your answers go directly into the system during install. The task files start with real content — your actual projects, your actual next actions — not empty templates. The system is useful from day one.

---

## What You'll Need to Do Yourself

The install is mostly a conversation. The main thing you need to bring is honesty — the more real your answers to the setup questions, the more useful your task system will be from the start.

After that, the habit is the work. A GTD system only works if you:

- **Capture** everything as it comes up — brain dump into the inbox, don't try to organize on the fly
- **Process** your inbox regularly — run `/process` in Claude Code and Claude walks you through it
- **Review** once a week — run `/review` on whatever day you chose during setup

Without the weekly review, the system goes stale within a few weeks. With it, it stays trustworthy indefinitely.

---

## How to Know It's Working

Run `/process` in Claude Code with at least a few items in your inbox. Claude should walk you through each one, ask what it is and what the next step is, and route it to the right place. At the end, your inbox should be empty and those items should appear in your projects or next actions.

If that works, the system is doing what it's supposed to do.

---

## You've Done It

With all six nodes installed, your AIOS is fully operational. Run `/audit` to see your score across all five layers, and `/tune` to get recommendations on what to improve next.

The system you've built is yours. Keep using it, keep the context files current, and keep running the weekly review. That's all it takes to keep it working.
