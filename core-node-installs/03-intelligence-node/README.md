# 03 — Intelligence Node

> This is where Claude gets eyes on your business.

---

## What It Is

The Intelligence Node connects Claude to your actual business data. It pulls numbers from the tools you're already using — YouTube, Stripe, Gmail, Outlook, Fireflies — stores them locally, and gives Claude a live view of what's happening in your business every day.

Before this node, Claude knows about your business from what you've told it. After this node, it can see it.

---

## What It Does

This node installs collectors — small programs that run in the background and pull data from your connected tools on a schedule. Every morning, they update a snapshot of your business numbers. Claude reads that snapshot at the start of every session so it always has current information.

**What gets collected depends on what you connect:**

- **YouTube** — subscriber count, views, video performance
- **Stripe** — revenue, active customers
- **Gmail or Outlook** — your inbox, filtered down to the emails that actually matter
- **Fireflies** — your meeting transcripts and summaries

You only connect the tools you actually use. Claude skips everything else.

Once it's running, you also get a file called `reach/metrics.md` that Claude reads every session — a formatted snapshot of all your current numbers. When you run `/pulse`, that's where Claude pulls from.

---

## What Happens During Install

Open Claude Code and run:
```
/install core-node-installs/03-intelligence-node
```

Claude will ask what tools you use before doing anything. You'll confirm which sources to connect, and Claude will tell you exactly what it's going to set up — and what it's skipping. Then it walks you through each connection one at a time.

Some connections just need a key you copy and paste. Others (like Gmail or Outlook) need you to sign in through a browser once so Claude has permission to read your inbox. You only do this once — after that it's automatic.

Claude will also set up a daily schedule so everything runs automatically in the background without you having to think about it.

---

## What You'll Need to Do Yourself

For each tool you connect, you'll need to get an access key from that tool's settings or developer dashboard. Claude tells you exactly where to find it and what to look for — you don't need to know anything about APIs in advance.

For Gmail and Outlook, you'll need to authorize access through a browser sign-in. It takes about two minutes and only happens once.

---

## How to Know It's Working

After install, run `/pulse` in Claude Code. If it returns real numbers from your business — actual subscriber counts, actual revenue, actual email counts — the Intelligence Node is running.

If you see your data, you're good.

---

## Next Step

```
/install core-node-installs/04-coffee-debrief-node
```
