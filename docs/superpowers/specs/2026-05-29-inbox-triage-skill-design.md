# Inbox Triage Skill — Design Spec

**Date:** 2026-05-29
**Status:** Approved design, pre-implementation
**Owner:** Paul (PaulStanley0211)
**Layer:** CRAFT "A" (Actions), reading the "R" (Reach) Gmail data

---

## Purpose

A `/triage` skill that reads Paul's Gmail inbox, classifies each message by the Email Profile in `CLAUDE.md`, drafts replies in his voice for the ones that warrant a reply, and writes those drafts into his Gmail Drafts folder for review. It records time saved per run so a week of daily use produces a measurable proof number.

This is Paul's #1 priority and headline portfolio artifact: "an inbox-triage skill that handles my real recruiter and job threads, drafts replies in my voice, and proves measurable time saved over a week of daily use."

## Success criteria

- Run `/triage` daily for a week; each run classifies the inbox, drafts replies for qualifying mail, and writes them to Gmail Drafts.
- A weekly rollup reports total drafts created and estimated minutes saved.
- Nothing is ever sent automatically. The gray-zone (negotiations, declines, rejections, salary) is surfaced, never drafted.

## Scope decisions (locked)

- **Output:** reply drafts written into the Gmail Drafts folder, threaded to the original. Nothing auto-sends.
- **Coverage:** all "Draft"-bucket human mail per the `CLAUDE.md` Email Profile (recruiters, hiring managers, interview scheduling, application follow-ups, prospective clients, any real human with a genuine question). Ignore-bucket is skipped. Gray-zone is surfaced with context but never drafted.
- **Measurement:** per-run log rolling up to a weekly total, using a tunable minutes-per-draft estimate.
- **Trigger:** manual `/triage`. Automatic scheduling is deferred to the Mobile/Flow node.

## Approach

Hybrid: a `/triage` prompt-skill owns the judgment (final classification + voice drafting); small, tested Python utilities own the mechanical parts (fetch/refresh, noise pre-filter, Gmail draft creation, run logging). This fits the repo's conventions (collectors are Python, skills are prompt commands) and keeps brittle logic testable while leaving classification/voice to the model.

## Architecture & components

New directory `actions/triage/` (the "A" layer has no Python home yet):

1. **`actions/triage/emails.py`** — `get_candidates()`: refresh the inbox (run the existing collector), read `intel.db`, exclude already-triaged messages, return candidate rows (gmail id, thread id, message-id, sender, subject, body_preview, date).
2. **`actions/triage/prefilter.py`** — `prefilter(sender, subject) -> "ignore" | "candidate"`: deterministic noise heuristics only (no-reply addresses, newsletters, receipts, etc.). The nuanced ignore/draft/gray-zone decision stays with the model in the skill.
3. **`actions/triage/gmail_draft.py`** — `create_reply_draft(thread_id, to, subject, in_reply_to, references, body) -> draft_id`: build a properly threaded plain-text MIME reply and create it in Gmail Drafts. Supports `--dry-run` (build MIME, skip the API call) for tests.
4. **`actions/triage/runlog.py`** — `record_run(stats)` and `weekly_rollup()`: write a run row to `intel.db` and append a human-readable line to `tuning/triage/log.md`.
5. **`.claude/commands/triage.md`** — the orchestrator skill (frontmatter like the other commands: name, description, user_invocable, trigger `/triage`, version).

## Auth change (one-time)

Widen `reach/auth/gmail_auth.py` scopes from `["gmail.readonly"]` to `["gmail.readonly", "gmail.compose"]`, delete the old `token.json`, re-run auth once.

- `gmail.compose` is the minimal scope able to create drafts.
- It technically also permits sending, but the skill never calls send — it only creates drafts.
- `gmail.readonly` is retained so the collector can keep reading the inbox.

## Data model (extend `reach/collectors/db.py`, in `intel.db`)

- **`emails` (existing) — add `thread_id TEXT`.** Threading a reply draft into the original conversation requires the Gmail `threadId`, which the current collector does not store (it stores only the RFC `Message-ID` in `message_id`, which is what we need for the `In-Reply-To`/`References` headers). The collector (`reach/collectors/gmail.py`) already has `msg["threadId"]` in hand, so populating it is a one-line change. For the existing `intel.db`, run a migration: `ALTER TABLE emails ADD COLUMN thread_id TEXT`, then re-run the collector to backfill recent mail.
- **`triage_actions`** — `(id, message_id, classification, action, draft_id, run_date)`. Prevents re-processing the same email (joined on `emails.message_id`) and records what happened to each.
- **`triage_runs`** — `(id, run_date, seen, drafted, surfaced, ignored, est_minutes_saved, created_at)`. Powers the weekly rollup.

`get_candidates()` returns, per candidate: gmail id, `thread_id`, `message_id` (RFC Message-ID, for reply headers), sender, subject, body_preview, date.

## Triage flow (`/triage`)

1. **Refresh** — run the Gmail collector to pull the latest inbox into `intel.db`.
2. **Load candidates** — `get_candidates()` returns recent, not-yet-triaged mail with obvious noise pre-filtered out.
3. **Classify (model)** — apply the Email Profile to each candidate: ignore / draft / gray-zone.
4. **Draft (model)** — for "draft" items, write a reply in Paul's voice using `context/voice/samples.md` (warm, tight, no banned words, context-appropriate sign-off). Gray-zone items get a one-line "why it's sensitive" note and no draft.
5. **Review table** — present one table: sender, subject, classification, action, draft preview.
6. **Approval gate** — Paul approves all / picks a subset / edits inline / skips. Nothing touches Gmail before approval. This gate enforces the "draft, never auto-send" rule and protects the gray-zone.
7. **Execute** — approved drafts are written into Gmail Drafts via `create_reply_draft()`, threaded to the original. Gray-zone and ignore create nothing.
8. **Log** — `record_run()` writes stats, appends to `tuning/triage/log.md`, and prints the weekly rollup.

## Measurement

- Each drafted reply counts as a tunable estimate, default **6 minutes saved/draft** (an editable constant).
- Per-run record: date, seen, drafted, surfaced, est. minutes saved.
- Weekly rollup: total drafts and total minutes saved over the last 7 days — the proof number for "a week of daily use."
- Acceptance tracking (whether a draft was actually sent) is out of v1; the simpler per-run estimate was chosen. Easy to add later.

## Error handling (fail loud, never silent)

- Token missing or wrong scope → stop and print the exact re-auth command.
- A single draft fails to create → report which one, continue the rest, do not abort the run.
- No candidates → report "inbox clean, nothing to draft," still log a zero run.
- Collector/refresh fails → triage on existing `intel.db` data and flag that the refresh failed.

## Testing

TDD on the mechanical units:
- `prefilter` — table of `(sender, subject)` → expected bucket.
- `gmail_draft` MIME builder — correct threading headers (`In-Reply-To`, `References`), recipient, and `Re:` subject handling, via `--dry-run` (no API).
- `runlog` — run row written correctly; weekly rollup math correct.

Classification and voice are model judgment and not unit-tested; the human review gate plus a skill self-check are the safety net.

## Out of scope for v1 (YAGNI)

Auto-send, scheduling, acceptance tracking, non-Gmail sources, HTML/attachment drafting (plain-text replies only).
