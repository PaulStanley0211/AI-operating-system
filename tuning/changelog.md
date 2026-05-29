# Changelog
<!-- v1.0.0 -->

> Version history of this CRAFT workspace.
> Updated automatically when nodes are installed with `/install`.
> Update manually when you make significant changes.

---

## 2026-05-29

- Audit rubric rewritten to v2 (project-adapted, Foundation + Maturity model): `.claude/commands/audit.md`. Re-pointed every check to this project (triage, Gmail, time-saved, voice depth, triage cadence, audit trend), dropped template checks for unused features, and stopped awarding points for the cut mobile bot. v2 baseline: **81/100 (B)**. Headroom sits on the strategy: real drafts (A4/A5), daily-triage habit (F4), audit trend (T4), references (C5). Report: `tuning/audits/2026-05-29-audit-v2.md`.
- Audit run: 63/100 (v1 template rubric — pre-adaptation baseline). Top gap: the rubric measures a running-business AIOS (live metrics, briefs, Telegram bot) this project skips, and awards 5 pts for the cut mobile-bot scaffolding. Next: rewrite `/audit` to fit the project, then re-baseline. Report: `tuning/audits/2026-05-29-audit.md`.
- Built: `/triage` inbox-triage skill (Actions layer). Reads Gmail, classifies each email by the CLAUDE.md Email Profile (ignore / draft / gray-zone), drafts replies in Paul's voice into Gmail Drafts for review (never sends; gray-zone surfaced not drafted), and logs time saved with a weekly rollup. New: `actions/triage/` (prefilter, emails, gmail_draft, runlog) + `.claude/commands/triage.md`; `intel.db` gained `triage_actions`/`triage_runs` tables + `emails.thread_id`; Gmail OAuth widened to `gmail.compose`. 22 tests. Built via brainstorm→spec→plan→subagent-driven TDD (two-stage review per task); spec + plan in `docs/superpowers/`. First run: 44 seen, 0 drafted (the one real recruiter, Paulina/Eraneos, already handled in LinkedIn), 1 surfaced, 43 ignored. Post-run hardening: UTF-8 mode in skill (Windows cp1252 crash), stronger prefilter (jobagent/LinkedIn-notifs/newsletters) with a guard that real recruiter InMail is never filtered.
- Connected: Gmail (Intelligence Node / Reach layer, partial). Read-only OAuth (gmail.readonly), deps installed, data.db + intel.db initialized, collector pulled 46 recent emails into intel.db. credentials.json + token.json gitignored. Other collectors (YouTube/Stripe/Outlook/Fireflies/FX) intentionally skipped (not used). metrics.md left empty by design (it tracks business dashboards, not the inbox). Fixed a Windows cp1252 emoji-print crash in gmail_auth.py.
- Installed: Context Node v1.2.0
- Configuration: adapted for solo engineer at portfolio/learning stage (no live business). Filled identity.md, business.md (reframed as positioning), strategy.md (3 focuses: inbox-triage skill, compounding audit score, 5-min walkthrough), and CLAUDE.md (About Me, Business, Team, Strategy, Voice, Email Profile, Working Prefs). Voice rules + banned-words captured. Email triage defined with sensitive gray-zone (Paul writes those himself).
- Pending: real voice samples to paste into context/voice/samples.md; Claude history export to distill (threads: RAGsystem, Multiwork, Agents, AIOS build, Job Search Strategy); ChatGPT import skipped.
- Installed: Vault Node v1.1.0
- Configuration: solo (team.md kept minimal, no roles section); `.env` created with `GITHUB_TOKEN`; `origin` re-pointed to https://github.com/PaulStanley0211/AI-operating-system.git (token auth verified)

## v1.0.0 — Initial Setup

- CRAFT workspace initialized
- Vault Node installed
- All 12 skills available in `.claude/commands/`
- All 6 nodes available in `node-installs/`
