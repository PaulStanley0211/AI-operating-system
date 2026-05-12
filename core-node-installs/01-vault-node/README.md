# 01 — Vault Node

> Install this first. Everything else builds on top of it.

---

## What It Is

The Vault Node creates your AIOS workspace — the folder structure, the master context file, and all the foundational pieces that every other node attaches to. Think of it as setting up the skeleton before any muscle gets added.

Without this, the other nodes have nowhere to live.

---

## What It Does

When you install the Vault Node, Claude builds out your workspace structure, creates a file called CLAUDE.md (more on that below), and makes sure everything is in place for the nodes that come after it.

**CLAUDE.md is the most important file in your entire AIOS.** It's automatically loaded at the start of every Claude session. It tells Claude who you are, what your business does, what your priorities are, and how you like to work. The more accurate and honest it is, the smarter Claude will be from the very first message of every session.

The Vault Node installs CLAUDE.md with a template. Your job after install is to fill it in.

---

## What Happens During Install

Open Claude Code and run:
```
/install core-node-installs/01-vault-node
```

Claude will ask you a few questions before building anything:

- Whether you're working solo or have a team
- What operating system you're on
- Whether you already have a GitHub account and personal access token

Your answers configure the install. Business identity and context get filled in during the Context Node.

---

## What You'll Need to Do Yourself

After install, open CLAUDE.md and fill in the rest of it. There are sections for your business description, your team, your current strategy, how you communicate, and how you like to work with AI. None of it needs to be perfect on day one — but the more you put in, the more useful every Claude session becomes.

Come back and update it whenever your strategy shifts or something significant changes in the business.

---

## How to Know It's Working

Run `/start` in Claude Code. If Claude greets you by name, describes your business accurately, and mentions your current focus, the Vault Node is doing its job.

---

## Next Step

```
/install core-node-installs/02-context-node
```
