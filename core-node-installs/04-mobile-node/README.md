# 05 — Mobile Node

> Your AIOS in your pocket.

---

## What It Is

The Mobile Node creates a Telegram bot connected to your workspace. You can message it like you'd message a person — ask a business question, query your numbers, capture a task — and it responds based on your actual context and data.

It's how you access your AI when you're away from your desk.

---

## What It Does

Once this is set up, you have a private Telegram bot that:

- Answers business questions using your context and live data
- Responds in whatever style you set — short and direct, detailed, or conversational
- Lets you send voice notes that it transcribes and answers
- Accepts `/capture [task]` messages that go straight into your task inbox
- Only responds to you (or whoever you authorize) — everyone else gets locked out

The bot is stateless, meaning it doesn't carry memory between messages. It's best for single questions and quick lookups, not long back-and-forth sessions. For deeper work, use Claude Code on your computer.

---

## What Happens During Install

Open Claude Code and run:
```
/install core-node-installs/05-mobile-node
```

Claude will ask you a few things:

- Whether you've used Telegram before (and if you already have a bot)
- What you'll mainly use the bot for
- What response style you want
- Whether you want to be able to send voice notes
- Whether anyone else should have access

Based on your answers, Claude sets up the bot configuration and walks you through getting it connected.

---

## What You'll Need to Do Yourself

You'll need a Telegram account. If you don't have one, Claude will walk you through setting it up — it's free and takes a few minutes.

Then you'll create a bot through a Telegram service called BotFather. It sounds technical but it's just a conversation in Telegram — you follow the prompts and it gives you a code. Claude tells you exactly what to do.

You'll also need to find your Telegram chat ID (another quick lookup Claude guides you through), and if you want voice notes, you'll need one more API key from OpenAI. That part is optional.

---

## How to Know It's Working

Send a message to your bot in Telegram. It should respond within a few seconds.

Then try asking it something about your business — "What's my YouTube subscriber count?" or "What's my current strategy?" If it answers using your actual data and context, it's working.

Finally, try sending a message from a different account or having a friend message it. They should get "Access denied." If that works too, the security is set up correctly.

---

## Next Step

```
/install core-node-installs/06-productivity-node
```
