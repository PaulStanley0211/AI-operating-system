# Weekly Review Checklist
<!-- v1.1.0 -->

> Run with `/review` in Claude Code.
> **Friday ritual:** review + `/audit` + `/tune` collapse into one session (not three separate days). Takes 30–60 minutes.
> Cadence: Friday = the ritual. Weekend = thinking time. Monday = execution.
> A system you don't review is a system you don't trust.

---

## Phase 1 — GET CLEAR

Goal: zero inboxes. Nothing captured elsewhere that isn't in the system.

- [ ] Run `/process` on `flow/gtd/inbox.md`
- [ ] Check Gmail drafts for uncaptured commitments
- [ ] (If used) sweep phone notes into inbox
- [ ] Inbox = 0 ✅

---

## Phase 2 — GET CURRENT

Goal: every list is accurate. No stale items.

### Projects
- [ ] Does every active project have a next action in next-actions.md?
- [ ] Are any projects actually done? → Mark complete, move to Completed
- [ ] Are any projects stalled? → Mark on hold or delete
- [ ] Any new projects to add?

### Next Actions
- [ ] Remove items that are done or no longer relevant
- [ ] Surface items sitting 3+ weeks → project or someday/maybe?
- [ ] Add context tags to any untagged items

### Waiting For
- [ ] Any items overdue? → Follow up now
- [ ] Anything received? → Remove from list
- [ ] Add any new delegated items (e.g. recruiter replies pending)

### Someday / Maybe
- [ ] Anything worth activating this week? → Move to projects or next-actions
- [ ] Anything clearly never going to happen? → Delete

---

## Phase 3 — GET CREATIVE

Goal: catch what the task lists miss.

- [ ] Read `flow/gtd/areas.md` — for each area, anything missing from the system?
- [ ] Review the latest `/audit` top gaps — is the next maturity point being worked?
- [ ] Ask: "Is there anything I'm worried about that isn't in the system?"

### Trigger list (work scope)
Projects started but not tracked | Commitments to people | Recruiter threads awaiting a reply | Applications to follow up | Portfolio/demo items half-finished | Anyone I owe a response | Repos or writing I meant to ship

---

## Phase 4 — REBUILD

Goal: clear picture of the week ahead, and the system gets smarter.

- [ ] Run `python flow/refresh_dashboard.py`
- [ ] Run `/audit` — log the score; confirm it moved the right way
- [ ] Run `/tune` — capture one improvement for next week
- [ ] Review the dashboard — does it reflect reality?
- [ ] Choose the ONE most important project for the coming week
- [ ] Confirm that project has a clear next action

**This week's focus:** _______________

---

*Ritual complete. Weekend to think, Monday to execute. See you next Friday.*
