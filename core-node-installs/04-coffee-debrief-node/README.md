# 04 — Coffee Debrief Node

> By the time you sit down with coffee, you already know what happened yesterday.

---

## What It Is

The Coffee Debrief Node takes everything the Intelligence Node collects — your metrics, your emails, your meeting summaries — and turns it into a structured morning intelligence report. It generates a chart of your most important number, then sends the whole thing to your Telegram before you start your day.

Every morning. Automatically. Without you doing anything.

---

## What It Does

Each morning, after your data has been collected, this node pulls it all together and sends you a brief that covers:

- What happened yesterday in your business
- The numbers that moved — up or down
- The emails that actually matter, filtered from the noise
- What came up in recent meetings
- What deserves your attention today

Along with the brief, you get a chart image showing your most important metric over time. It all lands in your Telegram so you can read it from your phone before you're even at your desk.

Every brief is also saved in your workspace so you can look back and ask Claude questions like "what was happening in my business two weeks ago?" or "when did my subscriber count start dropping?"

---

## What Happens During Install

Open Claude Code and run:
```
/install core-node-installs/04-coffee-debrief-node
```

Claude will ask you a few things before setting anything up:

- Which AI you want generating your brief — there are two options, and Claude will explain the difference in plain terms
- How much detail you want — a quick 3-5 minute read, or a more thorough 8-10 minute one
- What the single most important number in your business is right now
- What time you want the brief delivered in the morning

Your answers configure the brief to match how you actually work.

The Mobile Node (Telegram bot) needs to be installed before the brief can be delivered to your phone. If you haven't done that yet, install it first and then come back.

---

## What You'll Need to Do Yourself

You'll need to get one API key to power the brief generation — Claude will tell you exactly where to get it and what to do with it. It takes about five minutes.

Everything else is set up automatically during install.

---

## How to Know It's Working

Run the brief manually after install — Claude will show you the command. If a brief shows up in your Telegram with a chart image attached, and it contains real information from your business, it's working.

The next morning, check if it arrived on time. If it did, you're done.

---

## Next Step

```
/install core-node-installs/05-mobile-node
```
