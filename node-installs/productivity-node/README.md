# Productivity Node

> Layer: F (Flow)
> GTD task management — capture everything, process it into action, review weekly.

---

## What It Is

The Productivity Node installs a complete GTD (Getting Things Done) system into your AIOS workspace. It gives Claude a structured place to manage everything you're working on: a capture inbox, active projects, next actions organized by context, delegated items, someday ideas, and a weekly review protocol.

If your head is full of things you're tracking, this is where you put them.

---

## What It Does

- Creates your GTD file system: inbox, projects, next-actions, waiting-for, someday-maybe, areas, dashboard
- Installs the `/process` command — Claude walks you through your inbox item by item until it's empty
- Installs the `/review` command — a guided 4-phase weekly review that takes 30–60 minutes
- Generates a GTD dashboard that shows your open projects, next actions, and overdue items
- Integrates with the Mobile Node: send `/capture [task]` from Telegram to add items remotely
- Installs scripts to auto-refresh the dashboard and append items to inbox programmatically

**GTD files installed:**

| File | Purpose |
|------|---------|
| `flow/gtd/inbox.md` | Raw capture bucket — dump everything here, sort later |
| `flow/gtd/projects.md` | All active projects with next action and outcome |
| `flow/gtd/next-actions.md` | Actions by context: @me, @claude, @calls, @errands |
| `flow/gtd/waiting-for.md` | Delegated items, owners, expected dates |
| `flow/gtd/someday-maybe.md` | Ideas and commitments for the future |
| `flow/gtd/areas.md` | Your areas of responsibility |
| `flow/gtd/dashboard.md` | Auto-generated operational overview |
| `flow/gtd/review-checklist.md` | Weekly review protocol |

---

## How to Install

With Vault Node already installed (Context is recommended but optional), run:
```
/install node-installs/productivity-node
```

Claude will ask you 6 setup questions:
1. What are the main areas of your life and work you're responsible for?
2. What are 3–5 real projects you're actively working on right now?
3. Anything sitting in your head right now that you've been meaning to do?
4. What day and time works best for your weekly review?
5. Any additional context tags beyond the defaults (@me, @claude, @calls, @errands)?
6. Do you use a physical notebook or anything offline to capture ideas?

Your answers are used to pre-fill projects.md, next-actions.md, and inbox.md with real content during install. The system starts lived-in, not empty.

---

## How to Know It's Working

After install, run a `/process` session in Claude Code:
```
/process
```

Claude should walk you through each item in inbox.md one at a time, asking what it is, what the next action is, and where it belongs. At the end, inbox.md should be empty and items should have moved to next-actions.md or projects.md.

Then run:
```bash
python flow/refresh_dashboard.py
```

Open `flow/gtd/dashboard.md` — it should show your current project count, next actions by context, and any overdue waiting-for items.

The system is working if:
- [ ] `/process` takes inbox to zero
- [ ] Items appear in next-actions.md with context tags
- [ ] Dashboard shows accurate counts
- [ ] `/review` walks through all 4 phases without errors

---

## What to Expect

GTD only works if you use it consistently. The install makes it easy to start — but the habit is what makes it valuable.

**The weekly review is the keystone habit.** Without it, next-actions gets stale, projects sit without updates, and the system stops being trustworthy. Set a recurring 45-minute block (Fridays work well for most people) and protect it.

The first few `/process` sessions will feel slow as you build the habit. After 2–3 weeks, you'll move through it quickly. After a month, you'll notice your head is clearer because you trust the system to hold everything you need to do.

If you have the Mobile Node installed, you can capture tasks from anywhere with `/capture [task]` in Telegram. Items land directly in inbox.md and wait for your next `/process` session.

---

## What You Have to Do Yourself

| Task | Frequency |
|------|-----------|
| Capture anything new to inbox.md | Whenever something comes up |
| Run `/process` to clear the inbox | A few times per week |
| Run `/review` for your weekly review | Once a week (30–60 min) |
| Update projects.md when projects complete or change | As needed |
| Update areas.md when your responsibilities shift | Occasionally |

The system doesn't automate your judgment — it gives your judgment a place to live. You still have to decide what matters and what to work on next. Claude helps you process and organize, but the calls are yours.

---

## Next Step

With all nodes installed, run your first audit:
```
/audit
```

Then set up a monthly tuning rhythm:
```
/tune
```
