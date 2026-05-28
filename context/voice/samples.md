# Voice Samples
<!-- v1.0.0 -->

> 5+ examples of your actual writing. The AI reads these to match your voice when drafting emails, posts, or any content.
> Use real writing — copy from emails you've sent, posts you've published, or messages you've written.
> Annotate each one with the tone and context so the AI understands when each style applies.

---

## Sample 1 — Reply to a recruiter (real, sent)

**Tone notes:** Warm, gracious, concise. Handles a soft rejection (language requirement) without friction. Polite but human, not stiff. Keeps the door open. Sign-off: "Kind regards, Paul". This is the gold-standard register for the inbox-triage skill's recruiter/hiring-manager drafts.

```
Hi Paulina,

Thank you for taking the time to reach out and explain. I completely understand the language requirement for client-facing roles, and I appreciate the transparency.

Eraneos is doing exactly the kind of Data & AI work I'm drawn to, so I'd genuinely welcome staying on your radar. If a role comes up that's English-speaking, less client-facing, or based out of the NL side, I'd love for you to keep me in mind.

Thanks again, and all the best from your side too.

Kind regards,
Paul
```

---

## Sample 2 — LinkedIn build-in-public post (real, published)

**Tone notes:** Public/broadcast register. Concrete and technical, anti-hype. Leads with what shipped, then numbered "things that surprised me" with the actual fix for each. Specifics over adjectives. Ends with a light, open invitation. Note his real casual sign-off here ("Happy to chat...") — fine in his own posts, but still avoid "I'll be happy to / I'd be delighted to" in drafted emails.

```
Shipped a social app this week using Convex, Clerk, and Anthropic's Claude Haiku.

Three things that surprised me along the way:

1. Convex has no UNIQUE constraint.
I needed unique usernames at signup. The fix: handle the index lookup, ownership check, and patch inside a single transaction. Concurrent claims retry safely via OCC. No race condition, no extra infrastructure.

2. Webhooks lie to you in development.
I built the billing flow trusting a Clerk → Convex webhook, then realized on deploy that webhooks don't fire without a public URL. Pivoted to a client-side useSubscription() hook plus a Convex action that pulls live state via Clerk's REST API. Cancel → Pro now flips to Free instantly. No webhook required.

3. Clerk dev keys don't work on real domains.
Free-tier pk_test_* keys are scoped to localhost. Going live needed a Clerk production instance plus DNS records pointing at clerk.<my-domain>. Painless once you know, easy to miss if you don't.

Stack: Next.js 16, Convex, Clerk, Tailwind 4, Claude Haiku, deployed on Vercel.

Live → rose.paulstanley.dev
Code → https://lnkd.in/dUwpJhMq

Happy to chat if you're building on a similar stack.

#BuildInPublic #WebDevelopment #NextJS #Convex #IndieHacker
```

---

## Sample 3 — [Casual / short reply]

**Tone notes:** Short, conversational.

```
[PASTE a real short message.]
```

---

## Sample 4 — Portfolio site copy (adapted from paulstanley.dev, his own words)

**Tone notes:** Direct, technically precise, deliberately unglamorous, anti-hype.

```
I build production-grade AI agent systems, not demos.

My path: mechanical engineer, then trader, now agent engineering. Each chapter
taught a different muscle: precision, decision-making under uncertainty, and the
discipline to ship. Trading taught me that decisions made under uncertainty need
rules, audit trails, and risk limits built in.

Let's build something that ships.
```

---

## Voice Summary

How to sound like Paul when drafting on his behalf:

- **Tone:** Warm and conversational, but in tight, short sentences. Polite without being formal. Sound like a human who respects the reader's time. For long-form / portfolio writing, lean direct, technically precise, and deliberately unglamorous (anti-hype).
- **Length:** Short by default. Say it and stop.
- **Openers:** Lead with the point. No "I hope this finds you well." No AI-flavored openers.
- **Punctuation:** **No em dashes.** Short sentences and short paragraphs instead.
- **Email structure (from the Paulina reply):** open with a genuine thanks / acknowledge their point, state your interest or ask plainly, warm close. No groveling, no over-formality.
- **Sign-off:** Context-dependent. Casual/short: just "Paul". Professional emails (recruiters, hiring managers, clients): "Kind regards, Paul".

### Never use these words/phrases

- Em dashes ( — )
- "delve into"
- "leverage" as a verb (use **"use"**)
- "robust"
- "cutting-edge"
- "game-changing"
- "synergy"
- "ecosystem"
- "I'll be happy to" / "I'd be delighted to"
- "essentially"
- "in today's fast-paced world"
- Marketing speak / vague generalities
- AI-flavored openers like "certainly" and "absolutely"
