# Context Node — Install Guide
<!-- v1.0.0 -->

> Layer: C (Context)
> Teaches the AI who you are, what your business does, and how to sound like you.

---

## What This Node Does

Completes the Context layer: fills in CRAFT.md, populates context/ files, imports conversation history, and sets up voice samples. After this node, the AI behaves like a senior team member from the first message of every session.

---

## Setup Questions

Ask these before doing anything. Use the answers to customize the context files and CRAFT.md.

1. **How would you describe your business to someone who's never heard of it? One or two sentences.**
   *(This becomes the core of context/business.md and CRAFT.md — get it right upfront)*

2. **Who is your customer and what problem do you solve for them?**
   *(Fills the customer persona and value prop sections in context/business.md)*

3. **Which email client do you use — Gmail, Outlook, or both?**
   *(Configures the email profile in CRAFT.md)*

4. **How would you describe your communication style? Pick the closest: Direct and brief / Warm and conversational / Detailed and thorough**
   *(Seeds the voice section — the AI will match this style when writing on your behalf)*

5. **Do you have existing AI conversation history to import — from Claude, ChatGPT, both, or neither?**
   *(Yes = run the relevant import scripts. No = skip that step entirely)*

6. **What are the 2–3 things you're most focused on right now in your business?**
   *(Pre-fills context/strategy.md so /start surfaces your real priorities immediately)*

Use these answers to fill in CRAFT.md and context/ files now — don't leave [FILL IN] markers for things the user just told you.

---

## Prerequisites

- [ ] Vault Node installed and CRAFT.md filled in
- [ ] Python 3.10+ installed
- [ ] Claude account (for conversation export) or ChatGPT account

---

## .env Variables Required

None for the core install. Optional:
| Variable | Description | Where to get it |
|----------|-------------|----------------|
| (None required) | — | — |

---

## Files Installed

| File | What it does |
|------|-------------|
| `context/identity.md` | Personal + professional profile |
| `context/business.md` | Company info, customers, pricing |
| `context/team.md` | Team members and roles |
| `context/strategy.md` | Current quarter priorities |
| `context/voice/samples.md` | 5+ writing samples for voice matching |
| `context/scripts/import_claude.py` | Imports Claude conversation export |
| `context/scripts/import_chatgpt.py` | Imports ChatGPT conversation export |

---

## CRAFT.md Updates

The following sections of CRAFT.md should be completed during this install:
- `## About Me`
- `## The Business`
- `## Team`
- `## Strategy This Quarter`
- `## Voice`
- `## Email Profile`
- `## Working Preferences`

---

## Setup Steps

1. **Fill in `context/identity.md`:**
   Open the file. Fill in every `[FILL IN]` section. Take your time — this is the AI's foundation.

2. **Fill in `context/business.md`:**
   What you sell, who you sell it to, pricing tiers, what makes you different.

3. **Fill in `context/team.md`:**
   If solo: "Team size: Just me." That's fine.

4. **Fill in `context/strategy.md`:**
   Your top 3 priorities this quarter and your key target metric.

5. **Add voice samples to `context/voice/samples.md`:**
   Paste 5 examples of your actual writing. Real emails, posts, or messages. Annotate each with tone notes.

6. **Export your Claude conversation history** (optional but recommended):
   - Claude.ai → Settings → Privacy → Export data → Download ZIP
   - Extract the ZIP — find `conversations.json`
   - Run: `python context/scripts/import_claude.py path/to/conversations.json`
   - Imports are saved to `context/references/conversations/claude/`

7. **Export ChatGPT history** (optional):
   - ChatGPT → Settings → Data Controls → Export data → Download ZIP
   - Extract → find `conversations.json`
   - Run: `python context/scripts/import_chatgpt.py path/to/conversations.json`
   - Imports saved to `context/references/conversations/chatgpt/`

8. **Update CRAFT.md:**
   Copy the key identity/business/email profile details into CRAFT.md so they load every session.

---

## Validation

Run `/start` in Claude Code. The session summary should now include:
- Your name and role (from identity.md)
- A one-line description of the business (from business.md)
- Your current top priority (from strategy.md)

Ask: "Write me a 3-sentence email to a prospective client." The response should match the tone in `context/voice/samples.md`.

---

## Next Steps

Connect data sources so the AI can see what's happening in your business:
```
/install core-node-installs/03-intelligence-node
```

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | Initial release | Core context layer |
