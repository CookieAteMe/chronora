# Chronora Restore Workflow Specification

## Overview

Chronora's restore workflow exists to recover **project continuity**, not to replay chat history.

When a new AI agent session starts, the goal is not to reconstruct every prior conversation turn. The goal is to rebuild the smallest correct working set needed to continue the project safely and efficiently.

Chronora therefore treats restore as a **continuity loading protocol**:

- load what is true now
- load what should happen next
- load what work is active
- load only the historical context that still matters
- consult raw history only when ambiguity or evidence requires it

This specification defines that protocol.

---

## 1. Restore Philosophy

## 1.1 Continuity, not transcript replay

The purpose of restore is to recover a usable project operating state.
It is not to replay every message, thought, or experiment from earlier sessions.

Transcript replay is the wrong default for long-running software work because it is:

- noisy
- expensive in context
- inconsistent across tools
- full of obsolete reasoning
- likely to mix old assumptions with current truth

Project continuity is a different target.
It asks:

- What is true now?
- What is the current objective?
- What is blocked?
- What should happen next?
- What historical context still matters?

Those are state questions, not replay questions.

## 1.2 Restore target

The restore target should be:

> the smallest correct working set that allows the next session to continue safely without rereading unnecessary history.

That working set should prioritize:

- live truth
- immediate action context
- active work state
- compressed historical background
- raw evidence only when needed

## 1.3 Deterministic restore

Chronora restore should be deterministic and file-driven.

It should not depend on:

- a model remembering prior chats
- hidden retrieval behavior
- replaying a vendor-specific transcript format

It should depend on explicit project state.

---

## 2. Restore Inputs

Each Chronora state artifact plays a different role during restore.

| Artifact | Role in restore | Priority | When to consult | If missing |
| --- | --- | --- | --- | --- |
| `current.md` | canonical live truth | highest | always | restore confidence drops sharply; reconstruct provisional truth |
| `handoff.md` | immediate next-session baton | very high | default after `current.md` | fall back to tasks + summaries |
| `tasks.md` | active work inventory and status | high | default in normal/deep restore | use next steps from `current.md` and summaries as fallback |
| `summaries/` | compressed historical context | medium | when history matters beyond immediate state | fall back to deeper archive inspection |
| `sessions/` | append-only evidence | lowest by default | ambiguity, verification, recovery, or deep restore | continue from surviving state with reduced evidence confidence |

## 2.1 `current.md`

`current.md` is the primary restore artifact.

It defines:

- what is true now
- active architecture constraints
- unresolved problems
- important decisions
- immediate next steps

Restore must begin here because no other artifact should outrank live truth.

## 2.2 `handoff.md`

`handoff.md` provides the shortest path to action.

It answers:

- what the current objective is
- what the next session should do first
- which constraints matter immediately
- which references are most relevant right now

It is the restore artifact most optimized for fast continuation.

## 2.3 `tasks.md`

`tasks.md` provides operational work state.

It clarifies:

- what is active
- what is blocked
- what is pending
- what work should be prioritized next

`tasks.md` becomes especially important when the next steps in `current.md` are too compact or when multiple workstreams exist.

## 2.4 `summaries/`

`summaries/` provides compressed historical context.

It explains:

- how the project reached its current state
- which decisions still matter from earlier work
- what historical changes remain relevant
- what older detail can safely stay compressed

Summaries should be consulted only to the degree needed.
They are not the starting point for routine restore.

## 2.5 `sessions/`

`sessions/` is the evidence layer.

It should answer questions such as:

- what changed in a specific session
- whether live state drifted incorrectly
- what the project state looked like before and after a session
- how to resolve ambiguity when higher-level artifacts disagree or are incomplete

It is the deepest and most expensive restore layer.

---

## 3. Restore Priority

Chronora should load restore state in a deliberate order.

Recommended default order:

```text
current.md
  -> handoff.md
    -> tasks.md
      -> highest useful summary layer
        -> session archives if needed
```

## 3.1 Why `current.md` comes first

`current.md` defines the live operating truth.
Restore that starts anywhere else risks loading obsolete or merely explanatory context before loading the facts that are supposed to be true now.

## 3.2 Why `handoff.md` comes second

Once live truth is loaded, the next question is not “what happened before?” but “what should happen next?”

That is the role of `handoff.md`.
It turns restored truth into immediate direction.

## 3.3 Why `tasks.md` comes third

After truth and immediate direction are known, restore should load the active work surface.

`tasks.md` provides:

- active task inventory
- blocked work
- operational priorities
- parallel work visibility

It gives the session a more complete work model without forcing a historical deep dive.

## 3.4 Why summaries come after canonical state

Summaries explain context.
They do not define live truth.

Loading them later prevents compressed history from overshadowing the canonical state that should govern present action.

## 3.5 Why archives come last

Archives are evidence, not the default working set.
They are the most expensive layer to inspect and should only be loaded when:

- ambiguity remains
- verification is needed
- state is missing or inconsistent
- deep restore is explicitly requested

## 3.6 Why restore should not start from summaries or archives

Starting from summaries or archives would bias restore toward historical narration instead of present continuity.
Chronora should always rebuild from the current state outward, not from the past inward.

---

## 4. Restore Profiles

Chronora should support three conceptual restore modes.

## 4.1 Fast Restore

### Purpose

Fast Restore is for quick continuation under tight context limits or low ambiguity.

### Recommended inputs

- `current.md`
- `handoff.md`
- only the most relevant active tasks or task subset

### Use when

- the project is already in a stable active flow
- the handoff is fresh
- the objective is narrow and well-understood
- historical ambiguity is low

### Trade-off

Fast Restore minimizes token cost, but it carries the highest risk of missing deeper background.

---

## 4.2 Normal Restore

### Purpose

Normal Restore should be the default restore mode.

### Recommended inputs

- `current.md`
- `handoff.md`
- `tasks.md`
- the highest useful summary layer

### Use when

- the project is active and healthy
- one summary layer is enough for context
- there is no obvious drift or contradiction

### Trade-off

Normal Restore balances context cost and continuity confidence.

---

## 4.3 Deep Restore

### Purpose

Deep Restore is for ambiguous, stale, degraded, or long-gap situations.

### Recommended inputs

- `current.md`
- `handoff.md`
- `tasks.md`
- project / weekly / daily summaries as needed
- selected session archives for evidence

### Use when

- the handoff is stale or missing
- the project has been inactive for a long time
- canonical state looks inconsistent
- summaries are incomplete
- evidence is needed to repair drift
- a new session must regain confidence after historical complexity

### Trade-off

Deep Restore provides the highest continuity confidence but at the greatest reading and token cost.

---

## 5. Context Budget Strategy

Restore must assume that the next session has finite context.

## 5.1 Priority principle

When context is limited, Chronora should prioritize by:

1. operational immediacy
2. live truth correctness
3. active work relevance
4. compressed historical meaning
5. raw historical evidence

## 5.2 Context tiers

### Tier 1 — always try to preserve

- `current.md`
- the most important sections of `handoff.md`
- critical active tasks
- active blockers
- immediate constraints

### Tier 2 — preserve when possible

- one relevant summary layer
- related tasks that affect the same workstream
- recently changed important decisions

### Tier 3 — preserve only when needed

- older or lower-priority summaries
- completed tasks with residual context value
- secondary workstreams

### Tier 4 — omit unless ambiguity requires them

- raw session archives
- low-value historical detail
- redundant context already absorbed into canonical state

## 5.3 What to keep under tight context

Keep:

- what is true now
- what should happen next
- what is blocked
- what could cause the session to make an incorrect decision

## 5.4 What to drop under tight context

Drop first:

- redundant history
- stale handoff detail
- completed tasks without ongoing relevance
- low-priority summaries
- detailed archives

## 5.5 Context budget rule

Limited context should reduce **depth**, not **correctness**.
The system should load less history before it loads less truth.

---

## 6. Failure Recovery

Restore must degrade gracefully when parts of the continuity state are missing, stale, or damaged.

## 6.1 `current.md` missing

### Problem

The canonical live truth is unavailable.

### Recovery strategy

1. load `handoff.md` if available
2. load `tasks.md`
3. load highest useful summary layer
4. inspect recent archives for evidence
5. reconstruct provisional live truth explicitly
6. re-establish canonical `current.md` as soon as possible

### Rule

Missing `current.md` is a severe continuity failure, but not a reason to fall back to transcript replay.

---

## 6.2 `tasks.md` missing

### Recovery strategy

- use `current.md` next steps and active problems as provisional work surface
- use `handoff.md` for immediate task orientation
- consult summaries if multiple workstreams exist
- re-establish `tasks.md` explicitly when practical

---

## 6.3 `handoff.md` stale or missing

### Recovery strategy

- trust `current.md` as live truth
- use `tasks.md` to infer active work priority
- load the most relevant summary layer for near-term context
- create a fresh handoff later once current direction is clear

### Rule

A stale handoff should reduce action confidence, not overwrite canonical truth.

---

## 6.4 summaries missing

### Recovery strategy

- proceed from canonical state first
- use `tasks.md` and handoff for action context
- inspect archives more deeply when historical background matters
- regenerate historical compression later when appropriate

---

## 6.5 archive damaged or incomplete

### Recovery strategy

- continue from surviving canonical state and summaries
- treat archive confidence as degraded
- do not assume missing evidence invalidates live truth
- use remaining summaries and state to preserve continuity as best as possible

---

## 6.6 contradictory artifacts

### Recovery strategy

If artifacts disagree:

1. treat canonical live state as provisional operating truth
2. use summaries for context
3. inspect archives for evidence if needed
4. surface contradictions explicitly
5. correct canonical files deliberately rather than silently choosing one history source

---

## 7. Cross-Agent Restore

Cross-agent restore should follow the same continuity loading protocol regardless of which agent ended the prior session and which agent starts the next one.

## 7.1 Core rule

Cross-agent restore is not a special restore mode.
It is ordinary Chronora restore applied across a change in agent runtime.

What matters is not the prior agent identity.
What matters is the continuity state that survives it.

## 7.2 Claude -> Codex

Conceptually:

1. previous session leaves updated canonical state
2. summaries and archives preserve historical continuity
3. next session loads `current.md`, `handoff.md`, `tasks.md`, and relevant summaries
4. raw archive evidence is consulted only if needed

The restore protocol is the same as any other restore.

## 7.3 Codex -> Gemini

Conceptually identical:

- the new session does not need Codex transcript semantics
- it needs Chronora continuity state
- restore loads the same working set in the same order

## 7.4 Gemini -> Claude

Again, the continuity loading protocol does not change.

The session begins from:

- live truth
- immediate handoff
- work inventory
- compressed history
- evidence when needed

## 7.5 Why this matters

This is the architectural proof that Chronora restores **project continuity**, not **tool memory**.

---

## 8. Restore Lifecycle

Restore belongs to a larger continuity loop.

## 8.1 Session Start

At session start:

- restore loads the appropriate continuity inputs
- the next session receives a working set, not a transcript replay

## 8.2 Session Active

During the session:

- work happens inside restored continuity state
- live truth may evolve
- tasks may change status
- handoff direction may change

## 8.3 Current State Update

During or after work:

- `current.md` is updated when durable truth changes
- `tasks.md` is updated when work state changes
- `handoff.md` is updated when next-session guidance changes

## 8.4 Session End

When the session ends:

- the current live state is left as the next session’s starting truth
- append-only evidence should be preserved

## 8.5 Archive

Archive preserves before/after state transitions and historical evidence.
It is not the operating surface for the next session unless recovery requires it.

## 8.6 Summary Update

After sufficient history accumulates:

- summaries may be created or revised
- older detail may be compressed upward
- restore cost for future sessions should decrease

## 8.7 Next Session Start

The next restore begins again from canonical state, then immediate guidance, then work state, then compressed history, then evidence if needed.

## 8.8 Lifecycle rule

Restore is not a one-time import.
It is the opening step of every continuity loop.

---

## 9. CLI Vision

The following commands are future interface ideas only.
They are not current Chronora features.

## 9.1 `chronora restore`

Default restore workflow.

Conceptually:

- perform normal continuity loading
- present the default working set
- prefer canonical state and the highest useful summary layer

## 9.2 `chronora restore --fast`

Fast restore workflow.

Conceptually:

- prioritize the smallest useful working set
- load minimal immediate continuity inputs

## 9.3 `chronora restore --deep`

Deep restore workflow.

Conceptually:

- load broader continuity context
- descend further into summaries and archives
- use when ambiguity, long gaps, or degraded state exist

## 9.4 `chronora doctor`

State-health inspection workflow.

Conceptually inspect for:

- missing canonical files
- stale handoff
- missing summaries
- archive gaps
- contradictions between artifacts

## 9.5 Optional future directions

Possible future concepts, without committing to implementation:

- `chronora summarize`
- `chronora restore --from-summary <file>`
- `chronora doctor --repair-plan`

These ideas belong to future CLI design, not this specification.

---

## 10. Examples

## 10.1 Fast Restore example

A session resumes a narrow in-progress bug fix.

### Available state

- `current.md` says the auth bug is isolated and architecture is unchanged
- `handoff.md` says the next step is to validate one handler branch
- `tasks.md` contains many unrelated backlog items

### Restore behavior

- load `current.md`
- load `handoff.md`
- load only the active task relevant to the auth bug
- skip summaries and archives unless confusion arises

### Result

The session starts quickly with a correct narrow working set.

---

## 10.2 Normal Restore example

A project has ongoing work across one active feature area with healthy state files.

### Available state

- `current.md` reflects live architecture and active problems
- `handoff.md` points to the next feature step
- `tasks.md` shows one in-progress task and one blocked dependent task
- a weekly summary explains the larger context of this milestone

### Restore behavior

- load `current.md`
- load `handoff.md`
- load `tasks.md`
- load the weekly summary
- ignore raw archives unless something appears inconsistent

### Result

The session regains both immediate direction and enough historical context without wasting tokens on evidence-level history.

---

## 10.3 Deep Restore example

A project has been inactive for weeks and the handoff is clearly stale.

### Available state

- `current.md` exists but may not reflect the latest corrected understanding
- `handoff.md` references next steps that are no longer obviously current
- several weekly summaries exist
- recent archives include a session where state may have drifted incorrectly

### Restore behavior

- load `current.md`
- load stale `handoff.md` but treat it cautiously
- load `tasks.md`
- load project summary, then the latest weekly summary
- inspect selected archives to verify where drift occurred
- reconstruct confident live truth
- explicitly correct canonical files for the next session

### Result

The session spends more context to regain continuity confidence and repair live-state drift without relying on transcript replay.

---

## 11. Recommended Decisions

1. Restore should target a **correct working set**, not historical replay.
2. Restore should start from:
   - `current.md`
   - `handoff.md`
   - `tasks.md`
   - highest useful summary layer
   - raw archives only if needed
3. Context limits should reduce historical depth before they reduce live-truth correctness.
4. Fast, Normal, and Deep restore should differ by loading depth, not by continuity principles.
5. Failure recovery should degrade gracefully into deeper history rather than abandoning deterministic state.
6. Cross-agent restore should be identical at the continuity layer because the state contract is agent-agnostic.
7. Restore should be treated as the opening phase of an ongoing continuity loop.

---

## Final Recommendation

Chronora should restore projects by loading the smallest correct continuity state, not by replaying the largest possible historical record.

That means:

- live truth first
- immediate action next
- work state after that
- compressed history only as needed
- evidence only when required

This restore model preserves determinism, keeps context costs under control, and makes continuity portable across sessions without depending on transcript memory.