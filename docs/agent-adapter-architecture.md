# Agent Adapter Architecture

## Overview

Chronora should evolve from a **Claude-first workflow implementation** into an **agent-agnostic continuity layer**.

The key architectural shift is this:

- **Chronora owns project continuity**
- **Agents consume project state**
- **Adapters translate between Chronora and each agent runtime**

This document defines the recommended architecture for that evolution.

It does **not** propose immediate code changes, adapter implementations, or a directory migration in the current phase.

---

## 1. Problem Statement

### Why AI coding workflow should not be bound to a single agent

A continuity system becomes fragile when it is tied to one coding agent's CLI, session model, or prompt conventions.

That coupling creates several problems:

1. **Vendor lock-in at the workflow layer**
   If project continuity is encoded in one agent's folder names, startup rules, or transcript assumptions, switching tools becomes expensive and error-prone.

2. **Session continuity becomes frontend-dependent**
   A project should still be resumable even if the next session uses a different agent from the previous one.

3. **Cross-agent workflows become awkward or impossible**
   If Claude owns the state, Codex or Gemini cannot naturally continue from the same operational truth. They can only inherit an approximation.

4. **Project memory gets confused with agent memory**
   Chat history is an execution trace, not a canonical state system. A project should not depend on one model's transcript behavior to preserve architecture decisions, blockers, or next steps.

5. **Infrastructure becomes harder to generalize**
   Any future support for Aider, OpenCode, or new agents will be delayed if the continuity model itself assumes Claude-specific lifecycle semantics.

### Why project state should be independent from the agent

Chronora already treats continuity as a **deterministic state problem** rather than a recall problem.

That logic becomes even more important in a multi-agent future.

Project state should be:

- explicit
- editable
- local-first
- inspectable
- independent of proprietary transcript formats
- stable across sessions, tools, and operators

In other words, the project should own its continuity layer.
The agent should only read from it, act within it, and write durable changes back through a normalized process.

---

## 2. Design Goals

Chronora's future adapter architecture should support the following goals.

### 2.1 Agent independence

Chronora Core should define continuity semantics once.
No agent should become the source of truth for project state.

### 2.2 Session continuity

A session should resume from explicit project state, not from the hope that a model remembers the right prior context.

### 2.3 Cross-agent workflow

Multiple agents should be able to participate in the same project's lifecycle over time:

- Claude Code today
- Codex CLI tomorrow
- Gemini CLI later
- Aider or OpenCode in specialized workflows

### 2.4 Deterministic project state

The system should preserve the current Chronora philosophy:

- one canonical mutable state layer
- append-only session history
- clear distinction between live truth and historical evidence

### 2.5 Local inspectability

The continuity mechanism should remain file-based and understandable without a hidden service.

### 2.6 Capability-aware integration

Different agents support different behaviors.
Chronora should not assume parity where parity does not exist.

### 2.7 Strict support signaling

Chronora should document architectural direction without claiming shipped support prematurely.
A designed adapter is not the same as a validated adapter.

### Non-goals for the current phase

This architecture document does **not** recommend doing the following now:

- implementing adapters
- rewriting the current runtime
- renaming `.claude/` immediately
- claiming Codex, Gemini, Aider, or OpenCode support before validation

---

## 3. Proposed Architecture

### 3.1 Architectural model

Chronora should be split conceptually into three layers:

1. **Chronora Core**
2. **Adapter Layer**
3. **Agent Runtime Layer**

Chronora Core owns the continuity model.
Adapters translate that model into the expectations of each agent runtime.
The runtime itself remains external.

### 3.2 ASCII architecture diagram

```text
+------------------------------------------------------------+
|                        Chronora Core                       |
|------------------------------------------------------------|
| - canonical project state                                  |
| - continuity contract                                      |
| - append-only archive model                                |
| - session metadata normalization                           |
| - handoff/context bundle generation                        |
| - capability negotiation                                   |
+-------------------------------+----------------------------+
                                |
                                v
+------------------------------------------------------------+
|                        Adapter Layer                       |
|------------------------------------------------------------|
| Claude Adapter | Codex Adapter | Gemini Adapter | Others   |
+--------+---------------+---------------+---------------+---+
         |               |               |               |
         v               v               v               v
   +-----------+   +-----------+   +-----------+   +-----------+
   | Claude    |   | Codex CLI |   | Gemini CLI|   | Aider /   |
   | Code      |   |           |   |           |   | OpenCode  |
   +-----------+   +-----------+   +-----------+   +-----------+
```

### 3.3 Core principle

The most important rule is:

> **Project state is adapter-agnostic. Agents are state consumers. Adapters are translation layers.**

This keeps continuity logic stable even when agent ecosystems change.

### 3.4 Chronora Core responsibilities

Chronora Core should own:

- the canonical state model
- the archive model
- normalized session metadata
- handoff packaging rules
- capability negotiation rules
- compatibility policy
- continuity semantics across sessions

Chronora Core should **not** own:

- vendor-specific CLI invocation details
- tool-specific prompt syntax
- assumptions about native resume support
- agent-specific patch formats

### 3.5 Adapter Layer responsibilities

Each adapter should:

- validate that the target runtime exists
- declare its capabilities honestly
- prepare Chronora state for that runtime
- start or resume the runtime when possible
- normalize session outcomes back into Chronora's archive model

Adapters should stay thin.
They should not become mini-frameworks with their own state semantics.

---

## 4. Agent Adapter Interface

The adapter interface should be minimal, capability-driven, and focused on continuity.

## 4.1 Recommended interface surface

### `id()`
Returns a stable adapter identifier.

Example:

- `claude-code`
- `codex-cli`
- `gemini-cli`
- `aider`
- `opencode`

### `capabilities()`
Returns the adapter's declared capability set.

This is the basis for feature negotiation and support-tier labeling.

### `validateEnvironment()`
Checks whether the required CLI or runtime is available and usable in the current environment.

### `prepareContext(projectState, archiveState, handoffSpec)`
Transforms Chronora-managed state into an agent-ingestible context package.

This may include:

- startup instructions
- references to canonical state files
- handoff summaries
- normalized session metadata
- adapter-specific context formatting

### `start(sessionSpec)`
Starts a fresh agent session against Chronora-managed project state.

### `resume(sessionSpec)`
Attempts to resume a prior session.

Important distinction:

- **Native resume**: the agent can reopen its own prior session state
- **Chronora resume**: Chronora reconstructs continuity from canonical state and archive even if the runtime has no native resume

This distinction should remain explicit in the architecture.

### `archive(sessionResult)`
Writes a normalized record of session outputs back into Chronora's archive model.

### `normalizeOutcome(runtimeResult)`
Converts tool-specific exit or result semantics into Chronora's common session result shape.

---

## 4.2 Interface design principles

### Keep the interface small

The goal is not to capture every possible agent behavior.
It is to define the minimal contract needed for continuity.

### Prefer capability negotiation over assumed parity

If one agent supports native resume and another does not, Chronora should model that difference explicitly rather than paper over it.

### Separate continuity from editing semantics

Patch generation, file editing style, or interactive UX differences are important, but secondary.
The continuity layer should first guarantee stable state handoff.

### Normalize outcomes, not transcripts

Chronora should normalize operational facts:

- when a session started
- when it ended
- what live state it started from
- what live state it ended with
- which adapter/runtime was used
- whether native resume was used

It should not require transcript portability across all tools.

---

## 5. Capability Model

Different coding agents expose very different runtime behaviors.
Chronora therefore needs a capability model rather than a one-size-fits-all abstraction.

## 5.1 Capability categories

Recommended capability dimensions:

1. **Native session support**
   Can the runtime represent a persistent session identity?

2. **Native resume support**
   Can the runtime reopen or continue a previous session directly?

3. **Context injection support**
   Can Chronora provide startup instructions, file references, or a handoff bundle in a reliable way?

4. **Patch/edit support**
   Can the runtime make structured edits or patches in a predictable form?

5. **Archive metadata support**
   Can Chronora capture enough runtime metadata to normalize the session?

6. **Transcript capture availability**
   Does the runtime expose transcript or log artifacts that can be preserved as optional evidence?

7. **Noninteractive/scriptable launch**
   Can the runtime be launched in a deterministic wrapper flow?

8. **Worktree/branch friendliness**
   Can the runtime operate cleanly in isolated worktrees or branch-based workflows?

9. **Deterministic handoff fidelity**
   How faithfully can the runtime consume Chronora's state and continue work from it?

## 5.2 Capability tiers

Chronora should distinguish at least three support levels.

### Baseline supported

The adapter can:

- load canonical project state
- inject continuity instructions reliably
- start a session deterministically
- archive a normalized session record

### Enhanced supported

In addition to baseline, the adapter may support:

- native resume
- richer transcript capture
- structured patch/export behavior
- stronger continuity fidelity

### Experimental / unvalidated

The adapter concept exists, but the capability surface is not yet verified.
This tier is important because roadmap direction should not be presented as production reality.

## 5.3 Illustrative capability matrix

The matrix below is architectural, not a claim of shipped support.
Future rows should remain explicitly marked as planned until validated.

| Runtime | Native session | Native resume | Context injection | Patch/edit flow | Archive metadata | Transcript capture | Scriptable launch | Handoff fidelity | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Claude Code | Yes | Yes/strong | Strong | Strong | Strong | Medium/strong | Strong | High | Current production path |
| Codex CLI | To validate | To validate | Expected | To validate | Expected | To validate | Expected | Medium? | Planned |
| Gemini CLI | To validate | To validate | Expected | To validate | Expected | To validate | Expected | Medium? | Planned |
| Aider | To validate | To validate | Expected | Strong? | To validate | To validate | Expected | Medium? | Planned |
| OpenCode | To validate | To validate | Expected | To validate | To validate | To validate | Expected | Medium? | Planned |

The key purpose of this matrix is to prevent false equivalence.

---

## 6. State Directory Evolution

## 6.1 Current state

Chronora currently uses a Claude-first on-disk namespace:

```text
.claude/
  current.md
  CLAUDE.local.md
  sessions/
```

This matches the current implementation reality and should remain the documented truth for v0.1.

## 6.2 Future question: should Chronora migrate to `.chronora/`?

Long-term, a neutral namespace like `.chronora/` is architecturally attractive.
But naming cleanliness alone is not enough reason to migrate immediately.

## 6.3 Benefits of keeping `.claude/` for now

- zero migration cost in the current phase
- no breakage for existing users
- no mismatch with current shipped behavior
- no need for compatibility layers yet
- documentation remains aligned with implementation reality

## 6.4 Drawbacks of keeping `.claude/`

- agent-specific naming leaks into the continuity layer
- reinforces Claude-first perception
- creates conceptual tension once multiple adapters exist

## 6.5 Benefits of eventually moving to `.chronora/`

- cleaner product identity
- clearer separation between continuity infrastructure and agent runtime
- better fit for multi-agent workflows
- easier to explain that state belongs to the project, not to Claude

## 6.6 Drawbacks of migrating too early

- migration tooling would be required
- dual-path compatibility would add complexity
- existing docs/examples would need updates
- users could end up with split state between `.claude/` and `.chronora/`
- effort might be spent on naming before adapter behavior is proven

## 6.7 Recommended decision

**Do not migrate directories in the current phase.**

Recommended staged approach:

1. keep `.claude/` as the current runtime layout in v0.x
2. define a **logical Chronora state model** that is independent from the directory name
3. introduce migration support only after adapter abstractions are real
4. consider `.chronora/` as a future default only when backward compatibility is clear and low-risk

This preserves implementation honesty while keeping architectural direction open.

---

## 7. Cross-Agent Continuity

Cross-agent continuity should be built on **shared project state**, not shared proprietary transcripts.

## 7.1 Source of truth

The continuity source of truth should be:

- canonical live state
- normalized session metadata
- append-only archive snapshots
- a generated handoff/context bundle

It should **not** be:

- a vendor-specific transcript format
- one agent's internal session ID
- one runtime's prompt conventions

## 7.2 Continuity mechanism

A cross-agent handoff should work like this:

1. Agent A works from Chronora-managed state.
2. Chronora archives the session in a normalized form.
3. Chronora generates or exposes the latest handoff context from canonical state plus recent archive evidence.
4. Agent B starts from that same project truth through its adapter.
5. Agent B updates the same continuity layer rather than creating a separate memory island.

## 7.3 Example flow: Claude → Codex → Gemini

### Step 1: Claude session

- Claude Code starts from the project's current live state
- work progresses
- durable facts are written back to canonical state
- Chronora records normalized session metadata and archive snapshots

### Step 2: Codex session

- Codex adapter reads the same canonical state
- Codex adapter reads the latest normalized archive metadata
- Codex adapter prepares a Codex-friendly handoff bundle
- Codex continues from project truth, not from Claude-specific transcript memory

### Step 3: Gemini session

- Gemini adapter follows the same contract
- Gemini consumes the same canonical state and handoff bundle
- Gemini contributes changes back through the same continuity layer

## 7.4 Practical implication

Cross-agent continuity should be **Chronora-mediated**, not agent-to-agent.

That is the architectural move that keeps the system scalable as more runtimes are added.

---

## 8. Migration Plan

## v0.1

- Keep the current Claude-first implementation
- Clarify the long-term architecture in documentation
- Make no support claims beyond Claude Code

## v0.2

- Formalize Chronora Core concepts in docs/spec form
- Define adapter contract and capability model
- Define normalized session metadata expectations

## v0.3

- Refactor the current Claude path behind an internal adapter boundary
- Preserve current user-facing behavior
- Avoid changing state layout by default

## v0.4

- Add one experimental non-Claude adapter
- Validate cross-agent handoff using the same canonical state model
- Refine the capability matrix based on real constraints

## v1.0

- Ship a stable agent-agnostic continuity layer
- Publish compatibility tiers for supported runtimes
- Re-evaluate whether `.chronora/` should become the default namespace
- Keep any namespace migration backward-compatible and explicit

---

## 9. Risk Analysis

## 9.1 Over-generalizing too early

A universal interface designed before real adapter experiments may become abstract in the wrong places.

**Mitigation:**
Keep the core contract minimal and validate against real adapters incrementally.

## 9.2 Leaking Claude assumptions into the universal model

If the interface mirrors Claude-specific behavior too closely, future adapters will either become awkward or misleading.

**Mitigation:**
Separate Chronora continuity semantics from runtime-specific lifecycle semantics.

## 9.3 Claiming compatibility before validation

A roadmap can easily be mistaken for a support matrix.

**Mitigation:**
Use explicit support tiers such as production, experimental, planned, and unvalidated.

## 9.4 Confusing native resume with continuity resume

Some tools may not resume their own sessions, but can still continue project work from canonical state.

**Mitigation:**
Model these as different capabilities.

## 9.5 Namespace migration churn

Moving to `.chronora/` too early could create confusion, duplicated state, and unnecessary migration work.

**Mitigation:**
Delay physical migration until adapter behavior and compatibility policy are mature.

## 9.6 Archive bloat or overfitting

If the archive model tries to preserve every runtime's unique transcript semantics, it may become too complex to stay inspectable.

**Mitigation:**
Normalize operational facts first. Keep runtime-specific artifacts optional and secondary.

---

## 10. Recommended Strategy

The recommended path is:

1. treat **Chronora Core** as the owner of project continuity semantics
2. treat agents as **state consumers**, not as continuity owners
3. implement adapters later as **thin capability-declared translators**
4. keep the current `.claude/` runtime layout for now
5. design the logical state model before any physical namespace migration
6. build cross-agent continuity on normalized state and handoff bundles, not transcript portability
7. land architecture and documentation before runtime abstraction work

This strategy preserves Chronora's current strengths:

- deterministic state
- append-only history
- local inspectability
- simple operational model

while opening a credible path toward multi-agent continuity.

---

## 11. Recommended Implementation Order

This section is intentionally future-facing.
It describes the recommended order of work after architecture is accepted.

1. **Finalize the architecture document**
2. **Define the logical Chronora state contract**
3. **Define normalized session metadata and archive expectations**
4. **Define adapter interface and capability descriptors**
5. **Refactor the existing Claude path behind that interface without changing behavior**
6. **Validate one non-Claude adapter experimentally**
7. **Re-evaluate namespace migration only after adapter reality is proven**

---

## Final Recommendation

Chronora should not evolve by teaching every agent to own continuity.
It should evolve by making continuity a project-level system with adapters at the edge.

That means the right architecture is:

- **Core-owned state**
- **Adapter-mediated runtime integration**
- **Capability-aware support tiers**
- **Cross-agent continuity through shared deterministic state**

This gives Chronora the best chance to become a real **Agent-Agnostic Continuity Layer** without losing the clarity and inspectability that make the current design strong.