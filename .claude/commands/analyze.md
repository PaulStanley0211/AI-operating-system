---
name: analyze
description: Deep analysis of a task, system, or business problem. Grounded in CRAFT.md context. Usage: /analyze [topic or problem]
user_invocable: true
trigger: /analyze
version: 1.0.0
---

# /analyze — Deep Analysis

## Step 1: Read Context

Before analyzing anything, read:
- `CRAFT.md` — identity, business, email profile, working preferences
- `reach/metrics.md` — current metrics (if exists and relevant to the topic)

## Step 2: Parse the Topic

Extract the topic from the user's command. 

If the topic is fewer than 4 words or genuinely ambiguous (e.g., `/analyze my business`), ask one clarifying question before proceeding:
- "What specific aspect of [topic] do you want me to analyze?"
- "What's the outcome you're trying to reach with this analysis?"

If the topic is specific enough (5+ words, clear subject), proceed immediately without asking.

## Step 3: Determine Analysis Type

Choose the analysis type based on the topic:

| If the topic is about... | Use this type |
|--------------------------|--------------|
| Whether to automate a task | Task analysis |
| Understanding a system's strengths/gaps | System analysis |
| A business problem or its root cause | Problem analysis |
| A new opportunity or initiative | Opportunity analysis |

## Step 4: Produce the Analysis

Use this format exactly:

```markdown
## Analysis: [Topic]

### Context
[1–2 sentences on why this matters, grounded in what you know about the business from CRAFT.md]

### Findings
- [Most important finding]
- [Second finding]
- [Third finding]
- [Fourth if relevant — don't pad]

### Options
| Option | Upside | Downside | Effort |
|--------|--------|----------|--------|
| [A] | ... | ... | Low/Med/High |
| [B] | ... | ... | Low/Med/High |
| [C if relevant] | ... | ... | ... |

### Recommendation
[One clear, opinionated recommendation with the reason. Don't hedge. If the answer is obvious, say so directly.]
```

## Step 5: Close with Next Step

If action is likely appropriate, end with:
```
To move forward: `/plan [topic]`
```

If the analysis concludes "don't do this," skip the prompt.

## Behavior Rules

- Be specific, not generic. Use what you know about the business from CRAFT.md.
- The recommendation must be opinionated. "It depends" is not a recommendation.
- If data would strengthen the analysis but isn't available, say so: "I don't have current revenue data — connect Stripe in the Intelligence Node to get this."
- Target length: 300–500 words. Dense and useful.
- Match format preference from CRAFT.md working preferences.
