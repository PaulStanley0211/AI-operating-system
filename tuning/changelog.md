# Changelog
<!-- v1.0.0 -->

> Version history of this CRAFT workspace.
> Updated automatically when nodes are installed with `/install`.
> Update manually when you make significant changes.

---

## 2026-05-29

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
