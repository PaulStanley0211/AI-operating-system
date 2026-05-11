# 02 — Context Node

> This is where Claude stops being a generic AI and starts being YOUR AI.

---

## What It Is

The Context Node fills in the deeper knowledge that makes Claude genuinely useful for your specific business. After this node, Claude knows who your customers are, what you sell, how you communicate, and what you're focused on right now. It doesn't need to ask. It already knows.

---

## What It Does

This node creates a set of files in your workspace that Claude reads every session:

- **Who you are** — your role, your background, how you got here
- **Your business** — what you sell, who buys it, what makes you different
- **Your team** — who does what (or that it's just you, which is completely fine)
- **Your strategy** — what you're focused on this quarter
- **Your voice** — how you communicate, so Claude can write in your tone when you ask it to

It also gives you the option to bring in your existing AI conversation history from Claude or ChatGPT. If you've been using AI for a while, that history is full of useful context about how you think and what you've already figured out. Claude can learn from it.

---

## What Happens During Install

Open Claude Code and run:
```
/install core-node-installs/02-context-node
```

Claude will have a conversation with you — asking about your business, your customers, your communication style, and what you're working on right now. It uses your answers to fill in all the context files during install. By the time it's done, you should see real content, not placeholder text.

The better you answer the questions, the more useful your AIOS becomes. Don't overthink it — just answer honestly.

---

## What You'll Need to Do Yourself

**Add writing samples.** Claude can match your voice when writing emails, content, or messages — but only if you give it examples of how you actually write. After install, paste a few real emails or messages you've sent into `context/voice/samples.md`. The more real and varied, the better.

**Review what Claude filled in.** Claude does a solid first pass based on your answers, but you know your business better than any AI. Read through the context files and correct anything that's off.

**Update strategy quarterly.** The `context/strategy.md` file reflects what you're focused on right now. It goes stale if you don't update it when your priorities shift.

---

## How to Know It's Working

Ask Claude to write you a short email to a prospective client. If the tone sounds like you — not like a generic marketing email — the Context Node is working.

Run `/start` and check that the session summary mentions your business, your role, and your current top priority accurately.

---

## Next Step

```
/install core-node-installs/03-intelligence-node
```
