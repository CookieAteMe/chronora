# Chronora Core State Contract

## Overview

Chronora should manage **project continuity state**, not agent-specific memory.

The purpose of the Chronora State Contract is to define a shared, deterministic, human-readable protocol for long-running software work. Any future agent integration should consume the same state model rather than invent its own continuity system.

This contract is intentionally:

- **agent-agnostic**
- **deterministic**
- **human-readable**
- **Git-friendly**

It defines what Chronora manages, what counts as canonical state, what counts as historical evidence, and how those layers evolve over time.

This document is architectural only. It does **not** implement runtime behavior or claim additional agent support.

---

## 1. Design Principles

### 1.1 Agent-agnostic

State does not belong to any single coding agent.
It belongs to the project.

Agents are state consumers.
They read project continuity state, act within that context, and write durable changes back through a normalized workflow.

### 1.2 Deterministic

Project truth must exist explicitly in files.
It must not depend on chat history, model recall, or proprietary session memory.

### 1.3 Human-readable

All canonical state files must be readable and editable directly by developers.
Markdown is the default format because it is easy to inspect, discuss, diff, and repair.

### 1.4 Git-friendly

State files should be compact, low-noise, and stable enough for version control.
The contract should prefer simple sectioned Markdown over opaque or over-structured formats.

### 1.5 Live truth vs history separation

Chronora should preserve a hard boundary between:

- **live truth** — what the project should treat as true now
- **work state** — what is being done next
- **handoff state** — what the next session should understand immediately
- **history** — what happened during earlier sessions

This separation prevents old reasoning from being mistaken for current fact.

### 1.6 Minimal canonical set

The canonical mutable state should stay small.
Chronora should not accumulate dozens of state files when a few clear files are enough.

---

## 2. State Model Overview

Chronora's core state contract should consist of the following artifacts.

### Canonical mutable state

These files represent the current operational truth of the project:

- `current.md`
- `tasks.md`
- `handoff.md`

### Derived historical compression

These artifacts compress prior work into durable summaries:

- `summaries/`

### Append-only evidence

These artifacts preserve before/after session history:

- `sessions/` (or the current equivalent archive location)

## 2.1 Role definitions

### `current.md`
What is true now about the project.

### `tasks.md`
What work exists, what is active, and what is blocked or complete.

### `handoff.md`
What the next session should understand immediately before acting.

### `summaries/`
Compressed historical continuity artifacts derived from prior sessions or groups of sessions.

### `sessions/`
Append-only evidence of session state transitions.
This is history, not canonical truth.

---

## 3. `current.md`

## 3.1 Purpose

`current.md` is the canonical description of the project's current live state.

It should answer questions like:

- What is the project status right now?
- What architecture is currently in effect?
- What problems are still active?
- Which decisions should future sessions treat as settled?
- What should happen next?

## 3.2 Standard structure

Chronora should preserve the current v0.1 shape because it is already compact and readable.

Recommended standard structure:

```md
# Current Project

## Project Status

## Architecture

## Active Problems

## Important Decisions

## Next Steps
```

## 3.3 Required sections

The following sections should be required in contract v1:

- `## Project Status`
- `## Architecture`
- `## Active Problems`
- `## Important Decisions`
- `## Next Steps`

## 3.4 Recommended optional sections

These sections should remain optional and only appear when useful:

- `## Scope Boundaries`
- `## Known Risks`
- `## Open Questions`
- `## External Constraints`
- `## Dependencies`

The contract should resist making too many sections mandatory.
A bloated state file is harder to maintain and easier to ignore.

## 3.5 Content expectations

`current.md` should contain:

- concise status statements
- active architectural truth
- unresolved blockers that still matter
- durable decisions that shape future work
- a short list of concrete next steps

`current.md` should not contain:

- long transcript excerpts
- raw brainstorming
- verbose logs
- stale decisions that no longer apply
- duplicate task lists better kept in `tasks.md`

## 3.6 Update rules

Recommended update rules:

1. Update `current.md` when durable truth changes.
2. Remove stale facts instead of accumulating them forever.
3. Prefer conclusions over reasoning transcripts.
4. Prefer bullets or short paragraphs over large narrative blocks.
5. Keep the file short enough to review at session start.
6. Treat it as live truth, not as a historical record.

## 3.7 Format recommendation

For v1, `current.md` should stay as plain sectioned Markdown.

Avoid mandatory frontmatter unless future tooling proves that it is necessary.
The current structure is already highly readable and Git-friendly.

---

## 4. `tasks.md`

## 4.1 Purpose

`tasks.md` is the canonical operational work queue.

It should answer:

- What work exists?
- What is in progress?
- What is blocked?
- What is done?
- What should be prioritized next?

## 4.2 Standard structure

Recommended structure:

```md
# Tasks

## Backlog

## In Progress

## Blocked

## Done

## Dropped
```

The `Dropped` section is optional but recommended when abandoned work needs an explicit record.

## 4.3 Task record format

Each task should be represented as a compact Markdown block or bullet item with stable fields.

Recommended fields:

- `ID`
- `Title`
- `Status`
- `Priority`
- `Owner` (optional)
- `Blocked by` (optional)
- `Notes` (optional)
- `Exit Criteria` (optional)

Example compact pattern:

```md
- T-003 — Add email validation
  - Status: in_progress
  - Priority: P1
  - Owner: unassigned
  - Blocked by: none
  - Exit Criteria: invalid emails rejected with 400
```

## 4.4 State model

Recommended task states for contract v1:

- `todo`
- `in_progress`
- `blocked`
- `done`
- `dropped`

These states should be explicit and human-readable.
Avoid overly granular workflow states until they are proven necessary.

## 4.5 Priority model

Recommended priority levels:

- `P0` — critical, continuity-blocking, or production-blocking
- `P1` — high priority
- `P2` — normal priority
- `P3` — low priority

This scale is compact enough for quick triage and stable enough for version control.

## 4.6 Task lifecycle

Recommended lifecycle transitions:

- `todo -> in_progress`
- `in_progress -> blocked`
- `blocked -> in_progress`
- `in_progress -> done`
- `todo -> dropped`
- `in_progress -> dropped`
- `blocked -> dropped`

The contract should allow movement back from `done` only when a task was closed incorrectly and needs reopening as an explicit human correction.

## 4.7 Update rules

Recommended rules:

1. Every active task should have a stable ID.
2. Task titles should describe outcomes, not vague activity.
3. Priority should reflect current importance, not historical importance.
4. Blocked tasks should say what they are blocked by.
5. Done tasks may be pruned later into summaries if the file becomes too noisy.
6. `tasks.md` should remain actionable rather than archival.

---

## 5. `summaries/`

## 5.1 Purpose

`summaries/` stores compressed historical continuity artifacts.

Its job is to reduce archive-reading cost without turning historical compression into canonical truth.

A summary should capture what still matters from a prior period, session cluster, milestone, or long-running workstream.

## 5.2 What summaries are not

Summaries are not:

- the current source of truth
- a replacement for `current.md`
- a duplicate task board
- a substitute for append-only archive evidence

## 5.3 Naming convention

Recommended naming conventions:

- `YYYY-MM-DD-<slug>.md`
- `YYYY-MM-DD_HH-MM-SS-<slug>.md` when multiple summaries on the same day are necessary

Examples:

- `2026-06-02-auth-mvp-rollup.md`
- `2026-06-02_18-30-session-cluster-summary.md`

The naming should stay sortable and diff-friendly.

## 5.4 Content contract

Recommended structure:

```md
# Summary

## Summary Scope

## Key Changes

## Durable Decisions

## Remaining Work

## Related Sessions
```

A good summary should explain:

- what period or scope it summarizes
- what changed in that period
- what durable decisions still matter
- what remains unresolved
- which session archives it was derived from

## 5.5 Retention strategy

Recommended retention policy:

- summaries are optional but useful
- create them when archive history becomes too expensive to inspect directly
- keep them concise
- allow newer rollups to supersede older summaries
- preserve archive evidence even when summaries supersede older compression

This means summaries are **derived and replaceable**, while archives remain **append-only evidence**.

---

## 6. `handoff.md`

## 6.1 Purpose

`handoff.md` is the latest explicit baton-pass for the next session.

It should be optimized for immediate operational continuity.

If `current.md` answers “what is true now,” then `handoff.md` answers:

- what should the next actor do first?
- what must they not miss?
- what constraints matter right away?

## 6.2 Role distinction

- `current.md` = live truth
- `tasks.md` = work inventory and status
- `handoff.md` = immediate transition guidance

## 6.3 Minimum information set

For v1, `handoff.md` should include at least:

- current objective
- status snapshot
- immediate next steps
- active constraints or warnings
- key references or files
- unresolved questions or blockers

## 6.4 Standard structure

Recommended structure:

```md
# Handoff

## Objective

## Current Situation

## Immediate Next Steps

## Constraints

## Key References

## Open Questions
```

## 6.5 Update rules

Recommended rules:

1. `handoff.md` should stay short and current-facing.
2. It may be rewritten more aggressively than `current.md`.
3. It should point to canonical truth rather than duplicate everything.
4. It should optimize for fast resumption by the next session.
5. It should not become a long-running historical log.

---

## 7. State Lifecycle

Chronora's state should move through a predictable lifecycle.

## 7.1 Create

At project bootstrap, Chronora should create the canonical mutable state files.

Initial set:

- `current.md`
- `tasks.md`
- `handoff.md`

Optional directories:

- `summaries/`
- `sessions/`

## 7.2 Update

During or after a session, live state changes should be reflected in canonical mutable files.

- `current.md` updates when durable truth changes
- `tasks.md` updates when work status changes
- `handoff.md` updates when the next-session baton changes

## 7.3 Archive

When a session ends, Chronora should preserve append-only evidence of state transitions.

This archive layer should remain historical evidence rather than becoming live truth.

## 7.4 Compress

When session history becomes costly to read directly, Chronora may distill it into `summaries/`.

Compression should retain durable meaning while reducing reading cost.

## 7.5 Restore

If canonical live state becomes wrong or incomplete, the project may restore correctness by inspecting historical evidence and updating the canonical files explicitly.

The key rule is:

- restore **from** archive evidence
- restore **into** canonical state
- do not treat historical evidence itself as the new live truth without explicit correction

## 7.6 Lifecycle by artifact class

### Canonical mutable state

- mutable
- current-facing
- compact
- frequently reviewed

### Derived summaries

- mutable or replaceable
- compression-focused
- secondary to canonical truth

### Append-only archive

- immutable in principle
- evidence-focused
- not the primary operating surface

---

## 8. Versioning

## 8.1 Purpose

The State Contract should have an explicit version so future evolutions can remain compatible and understandable.

## 8.2 Contract version model

Recommended model:

- `v1` — initial stable state contract
- `v2` — future incompatible structural revision

The version should apply to the **contract as a whole**, not to each file independently.

## 8.3 Compatibility rules

Recommended rules:

1. Additive guidance within the same version family should remain backward-compatible.
2. Renaming required sections or changing their semantics should require a major version bump.
3. Moving canonical files to a new namespace should be treated as a compatibility event.
4. Archive evidence should remain interpretable across contract versions whenever possible.

## 8.4 Metadata strategy

For the design phase, the version should be defined conceptually without over-specifying implementation details.

A future implementation may expose version information through:

- a contract marker file
- a small metadata section
- an optional version line in canonical files

However, v1 should prioritize readability over excessive metadata ceremony.

---

## 9. Repository Layout

## 9.1 Recommended logical layout

Long-term, the Chronora State Contract should map cleanly to a neutral namespace:

```text
.chronora/
├── current.md
├── tasks.md
├── handoff.md
├── summaries/
└── sessions/
```

This layout reflects the logical contract more clearly than an agent-specific namespace.

## 9.2 Current implementation reality

Today, Chronora still uses the Claude-first layout:

```text
.claude/
├── current.md
├── CLAUDE.local.md
└── sessions/
```

That remains the implementation truth in the current version of the project.

## 9.3 Recommended evolution path

Recommended path:

1. define the logical contract independently from the current runtime layout
2. preserve `.claude/` as the current shipped layout
3. add `tasks.md`, `handoff.md`, and `summaries/` conceptually to the contract first
4. design migration and compatibility rules before any physical rename to `.chronora/`
5. move namespaces only when runtime abstractions are mature

## 9.4 Important boundary

This document defines the **state contract**, not the migration mechanics.
It therefore describes `.chronora/` as the recommended future logical namespace, not as a claim that current runtime behavior has already changed.

---

## 10. Examples

## 10.1 Example `current.md`

```md
# Current Project

## Project Status

Authentication MVP is working locally. Registration flow is partially implemented and needs one more focused session.

## Architecture

- FastAPI backend with a single entry point in `src/main.py`
- Authentication logic is still intentionally kept in one module
- Continuity state is maintained through Chronora-managed project files

## Active Problems

- `/register` still accepts malformed email input
- No rate limiting exists on `/login`
- Integration coverage is missing for the login happy path

## Important Decisions

- Keep the auth flow in one module until API boundaries stabilize
- Preserve explicit Markdown state as the source of continuity truth
- Treat archive history as evidence, not as the live operating state

## Next Steps

1. Add email validation to `/register`
2. Add a basic rate-limit strategy for `/login`
3. Add one integration-style test for the login happy path
```

## 10.2 Example `tasks.md`

```md
# Tasks

## Backlog

- T-003 — Add rate limiting to login
  - Status: todo
  - Priority: P1
  - Owner: unassigned
  - Blocked by: none
  - Exit Criteria: repeated login attempts are throttled predictably

## In Progress

- T-002 — Add email validation to registration
  - Status: in_progress
  - Priority: P1
  - Owner: current-session
  - Blocked by: none
  - Exit Criteria: invalid emails return 400 with a clear validation message

## Blocked

- T-004 — Add login integration test
  - Status: blocked
  - Priority: P2
  - Owner: unassigned
  - Blocked by: T-003
  - Notes: test behavior depends on stable rate-limit design

## Done

- T-001 — Confirm local login MVP works end-to-end
  - Status: done
  - Priority: P1
  - Owner: prior-session
  - Notes: verified locally against the example app

## Dropped

- T-000 — Split auth into multiple modules immediately
  - Status: dropped
  - Priority: P3
  - Owner: none
  - Notes: deferred until API boundaries stabilize
```

## 10.3 Example `handoff.md`

```md
# Handoff

## Objective

Stabilize the authentication MVP enough that the next session can finish registration validation and start adding basic safety controls.

## Current Situation

Login works locally. Registration exists but still accepts malformed email input. No rate limiting or integration coverage exists yet.

## Immediate Next Steps

1. Add email validation to `/register`
2. Re-run local registration flow with valid and invalid inputs
3. Decide whether login rate limiting belongs in middleware or inline handler logic

## Constraints

- Keep the example intentionally small and easy to inspect
- Do not split auth into multiple modules yet
- Preserve compact Markdown state instead of moving details into transcripts

## Key References

- `src/main.py`
- `current.md`
- `tasks.md`
- latest session archive

## Open Questions

- Should login rate limiting be implemented in-process for the example, or described as a future boundary?
- Is one integration-style test enough for the next milestone, or should registration also get coverage?
```

---

## 11. Recommended Decisions

The recommended v1 State Contract is:

1. **Canonical mutable state** should be exactly:
   - `current.md`
   - `tasks.md`
   - `handoff.md`

2. **Derived historical compression** should live in:
   - `summaries/`

3. **Append-only evidence** should remain in:
   - `sessions/`

4. `current.md` should remain structurally close to the existing Chronora v0.1 shape.

5. `tasks.md` should use a compact Markdown task model with explicit status and priority.

6. `handoff.md` should optimize for fast next-session continuity rather than historical storage.

7. The State Contract should version slowly and preserve human readability over schema complexity.

8. `.chronora/` should be the future logical namespace for the contract, while `.claude/` remains the current implementation layout until migration is explicitly designed and validated.

---

## Final Recommendation

Chronora should define continuity around a small, explicit, human-readable state contract.

That contract should separate:

- current truth
- work state
- immediate handoff
- historical compression
- append-only evidence

This gives Chronora a stable project-level protocol that can outlast any single coding agent while preserving the simplicity, inspectability, and determinism that already define the project.