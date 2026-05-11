# Context Node

> Layer: C (Context)
> Teaches the AI who you are, what your business does, and how to sound like you.

---

## What It Is

The Context Node completes the C layer — the foundation of CRAFT. It fills in the detailed context files that every Claude session loads: your identity, your business, your team, your current strategy, and your writing voice.

After this node, Claude stops being a generic AI assistant and starts behaving like a senior team member who knows your business.

---

## What It Does

- Populates `context/identity.md` — who you are, your role, your background
- Populates `context/business.md` — what you sell, who your customers are, your pricing model
- Populates `context/team.md` — who's on your team (or confirms you're solo)
- Populates `context/strategy.md` — your current top priorities this quarter
- Adds voice samples to `context/voice/samples.md` so Claude can write in your tone
- Optionally imports your Claude or ChatGPT conversation history so the AI has reference material from your past sessions
- Updates CRAFT.md with all the key context so it loads automatically every session

---

## How to Install

With Vault Node already installed, run:
```
/install node-installs/context-node
```

Claude will ask you 6 setup questions:
1. How you'd describe your business in one or two sentences
2. Who your customer is and what problem you solve for them
3. Which email client you use (Gmail, Outlook, or both) — for email triage later
4. Your communication style (direct and brief / warm and conversational / detailed and thorough)
5. Whether you have AI conversation history to import (Claude or ChatGPT exports)
6. Your 2–3 biggest business priorities right now

Your answers are used to pre-fill all context files during install. You should see real content — not `[FILL IN]` markers — when the install finishes.

---

## How to Know It's Working

After install:

- [ ] `context/identity.md` has your actual name, role, and background filled in
- [ ] `context/business.md` describes your actual business and customers
- [ ] `context/strategy.md` shows your current top priorities
- [ ] `context/voice/samples.md` has at least one writing sample
- [ ] CRAFT.md `## About Me` and `## The Business` sections are complete

Run this test in Claude Code:
```
/start
```

The session summary should include your name, a description of your business, and your current top priority. If it says all three correctly, Context Node is working.

Ask Claude to write you a 3-sentence email to a prospective client. If the tone matches your communication style from the setup questions, voice is working.

---

## What to Expect

The Context Node is mostly a conversation — Claude asks questions, you answer, and Claude fills in the files. Most installs take 20–30 minutes including the conversation.

The more honestly you answer the setup questions, the more useful every future Claude session becomes. This isn't about sounding polished — it's about being accurate. "We're a 2-person shop that charges $2,000/month for implementation" is more useful than a carefully worded paragraph that could describe any company.

If you're importing conversation history, expect 2–5 minutes of processing time depending on export size. The import is optional but strongly recommended if you have 6+ months of AI conversations.

---

## What You Have to Do Yourself

| Task | Notes |
|------|-------|
| Answer the setup questions honestly | This is 80% of the value — don't rush it |
| Add voice samples | Paste real emails or messages you've written — not AI-generated content |
| Export conversation history (optional) | Claude.ai → Settings → Privacy → Export data |
| Review and edit context files after install | The AI's first-pass fills are good but you know your business better |

The context files are yours to edit any time. Update `context/strategy.md` each quarter. Update `context/business.md` when your offer changes. The AI is only as current as what's in those files.

---

## Next Step

Once Context is done:
```
/install core-node-installs/03-intelligence-node
```
