# Chronora

> An AI IDE Continuity Layer for deterministic, file-driven software development.
>
> [中文文档](README.zh-CN.md)

> **Coding agents do not primarily need better chat memory.**
>
> **They need deterministic project state.**

Chronora is AI development infrastructure for long-running coding sessions.

It provides a deterministic continuity layer between coding agents and a software project by moving critical context out of ephemeral chat windows and into explicit, versionable state files. The current repository ships a Claude Code adapter as the reference frontend, but the model is intentionally broader than any single tool vendor. Claude, Codex, OpenCode, and IDE-native agents are all frontends. The continuity layer is the system.

## Vision

Build a practical operating layer for AI-assisted software engineering where project continuity is explicit, inspectable, and durable.

The long-term goal is not to create a better prompt wrapper. The goal is to establish a stable state model for coding agents so they can work across many sessions, many tools, and eventually many cooperating agents without resetting architectural understanding every time a terminal closes.

## Why This Exists

AI coding tools are increasingly capable at local reasoning, code generation, and short-horizon execution. What they still lack is reliable project continuity.

In real software projects, the hard part is rarely producing the next twenty lines of code. The hard part is preserving:

- architecture decisions
- current constraints
- unresolved problems
- in-flight tasks
- session-to-session intent
- the difference between raw history and current truth

Without a deterministic continuity layer, the user becomes the only stable memory system in the loop.

## The Problem With Chat-Based AI Development

Chat-based development breaks down as projects become longer-lived and more stateful.

Common failure modes include:

- architectural decisions being re-litigated every session
- partially completed work being rediscovered instead of continued
- context being preserved only in long transcripts with poor editability
- important constraints being buried in token history rather than maintained as state
- agent behavior drifting when switching tools, models, or time windows

Chat history is useful as execution trace. It is a poor primary state store.

## Deterministic Project State

Chronora treats project continuity as a state management problem, not a conversation recall problem.

A deterministic project state has four properties:

1. **Explicit** — the important context is written down, not inferred from hidden history.
2. **Inspectable** — humans and agents can read the same source of truth.
3. **Editable** — project state can be corrected directly when reality changes.
4. **Versionable** — changes to state can be archived, diffed, and reviewed.

The state model is intentionally file-driven. In the full conceptual model, project continuity is decomposed into these artifact classes:

- `CLAUDE.local.md` or equivalent frontend-local instruction file
- `current.md` as the canonical mutable project state
- `tasks/` for durable work decomposition and ownership
- `summaries/` for compressed state snapshots across larger timelines
- `sessions/` as the append-only execution archive

The current reference implementation initializes `current.md` and `sessions/` today and is designed to evolve cleanly into the fuller state graph.

## Stateful AI Development

Stateful AI development means the agent does not begin from zero every time it starts.

Instead, the agent enters an existing operating context:

1. read the project-local operating rules
2. load the current state of the project
3. execute work against that state
4. update state when durable facts change
5. archive the session without overwriting history
6. allow the next session to resume from the updated state

This is closer to systems operation than chat continuation. The continuity mechanism is file-backed, deterministic, and intentionally boring.

## Architecture

Chronora is designed as an **AI IDE Continuity Layer**.

The frontend agent may change. The continuity contract should not.

### Logical state flow

```text
Claude Code / Codex / OpenCode / IDE Agent
                  |
                  v
         Project-local instructions
          (CLAUDE.local.md, etc.)
                  |
                  v
          Canonical project state
               (current.md)
                  |
                  v
        Structured execution state
         (tasks/ and summaries/)
                  |
                  v
         Append-only session history
               (sessions/)
```

### Current reference adapter

```text
cclaude
  -> ensures .claude/ exists
  -> materializes current.md and CLAUDE.local.md from templates
  -> creates a root-level convenience symlink
  -> snapshots before-state
  -> launches the coding frontend
  -> snapshots after-state
  -> appends session metadata
```

### Architectural stance

- the continuity layer owns state, not the frontend
- archives are append-only, never mutable truth
- summaries compress state, not identity
- project state must survive model swaps and process restarts
- the main repository `CLAUDE.md` remains untouched unless the project itself wants it changed

## Directory Structure

### Repository structure

```text
chronora/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .gitignore
├── install.sh
├── bin/
│   └── cclaude
├── templates/
│   ├── current.md
│   └── CLAUDE.local.md
├── docs/
│   ├── architecture.md
│   ├── workflow.md
│   └── migration.md
└── examples/
    └── project-example/
```

### State layout inside a target project

```text
your-project/
├── .claude/
│   ├── current.md
│   ├── CLAUDE.local.md
│   ├── sessions/
│   ├── tasks/       # optional / future-compatible state domain
│   └── summaries/   # optional / future-compatible state domain
└── CLAUDE.local.md -> .claude/CLAUDE.local.md
```

The current implementation materializes `current.md`, `CLAUDE.local.md`, and `sessions/`. The broader layout shows where task state and summary state fit as the system evolves.

## Workflow

The operating workflow is intentionally deterministic:

### 1. Bootstrap

Start the frontend adapter from a project root. The adapter initializes the continuity layer if it does not already exist.

### 2. Load State

The coding agent reads project-local instructions and the current project state before proposing changes.

### 3. Execute

The agent performs implementation, debugging, research, or refactoring work within the constraints described by the state.

### 4. Update Durable State

When a decision, blocker, or next-step meaningfully changes, the agent updates `current.md` rather than hoping the chat window will preserve it.

### 5. Compress

High-volume conversation is reduced into compact durable state. The system values editorial compression over transcript accumulation.

### 6. Archive

The session is written into an append-only archive so the working state can evolve without losing historical checkpoints.

### 7. Resume

A later session, possibly on a different day or with a different model, resumes from the same explicit state.

## Session Archive System

The session archive is an append-only record of how project state changed over time.

Each invocation creates a timestamped directory under `.claude/sessions/` containing:

- `current.before.md`
- `current.after.md`
- `CLAUDE.local.before.md`
- `CLAUDE.local.after.md`
- `session.meta`

This matters for three reasons:

1. **Auditability** — you can inspect how state changed.
2. **Debuggability** — you can understand what the agent believed before and after a run.
3. **Recoverability** — you do not lose continuity when the live state needs correction.

The archive is history. It is not the current operating truth.

## Summary Compression Philosophy

Long-running AI systems need compression, but compression should be intentional.

Chronora makes a sharp distinction between:

- **history** — what happened
- **summary** — what still matters
- **current state** — what the next agent must treat as true now

The goal of summarization is not to create a nicer transcript. The goal is to distill durable operational knowledge.

Good compression:

- removes conversational noise
- keeps decisions and constraints
- preserves actionable next steps
- reduces ambiguity for the next session

Bad compression:

- copies chat logs into state files
- stores every detail equally
- confuses outdated reasoning with current truth

As the system evolves, `summaries/` should become a formal compression layer above raw session history and below live state.

## Task Continuity

Coding agents do not just need memory of facts. They need continuity of work.

That means preserving:

- what is currently being worked on
- what is blocked
- what depends on what
- what the next agent should pick up
- what has been completed versus merely discussed

In the current phase, some of this can live in `current.md`. The longer-term path is a first-class `tasks/` state graph with ownership, dependencies, and execution metadata.

For long-running coding agents, task continuity is not a luxury. It is the shape of the work itself.

## Comparison

Deterministic state is not the only way to give AI systems memory, but it is unusually well-matched to software engineering.

| Approach | Core mechanism | Strength | Limitation for coding continuity |
| --- | --- | --- | --- |
| Chat history | Linear transcript | Zero setup, naturally available | Token-bounded, implicit, hard to edit, poor separation of history vs current truth |
| Cursor memory | Tool-managed assistant memory | Convenient for personalization and light hints | Not deterministic project runtime state; limited auditability |
| Mem0 | Semantic memory retrieval | Good for facts, preferences, cross-session recall | Still retrieval-centric rather than state-centric; weak for exact project truth |
| Vector memory | Embedding-based retrieval | Good at large-scale fuzzy recall | Non-deterministic recall, ranking ambiguity, poor fit for source-of-truth state |
| Chronora | Explicit files + append-only archive | Deterministic, inspectable, editable, versionable | Requires disciplined state maintenance |

Why does this matter so much for coding?

Because software projects are coordination systems, not just semantic search problems. They require explicit constraints, current truth, task handoff, and traceable evolution.

## Why Not Vector Memory

Vector memory is valuable for large-scale, fuzzy, cross-document semantic recall.

But that is not the main problem here.

In coding continuity, the important questions are usually not:

- “Did someone say something similar before?”
- “Which chunk ranks highest?”

The real questions are:

- “What is the current architecture decision?”
- “What is the actual blocker right now?”
- “What should the next agent treat as true?”
- “What changed in this session relative to the last one?”

Those are state questions, not retrieval questions.

Embedding recall is probabilistic. Project state should not be.

## Why `current.md` Is the Source of Truth

`current.md` exists to hold the small set of facts that the next coding session must load before doing meaningful work.

It is the source of truth because it is:

- directly editable when reality changes
- compact enough to remain readable
- explicit enough to be reviewed by humans
- stable across sessions and frontends

The archive answers: “How did we get here?”

`current.md` answers: “What is true here now?”

That boundary matters.

If a fact in a transcript conflicts with `current.md`, the transcript is historical context. `current.md` is the runtime truth until corrected.

## Philosophy

Chronora is driven by systems design instincts more than prompt engineering tricks.

### File-driven state

Important context should live in ordinary files so humans can inspect, diff, edit, review, and commit it directly.

### Append-only archive

History should accumulate rather than be rewritten. That is what makes debugging and long-horizon analysis possible.

### Explicit state

The system should not rely on implicit memory, black-box ranking, or lucky recall to carry critical project truth.

### Deterministic context

Regardless of context window size, transcript truncation, or frontend vendor, the next session should load the same operating state.

This is a conservative philosophy, but reliable engineering infrastructure is often conservative precisely because it is explicit.

## Installation

The current repository ships a macOS zsh reference adapter named `cclaude`.

```bash
git clone <repo-url>
cd chronora
./install.sh
```

The installer will:

- copy `cclaude` to `~/bin`
- mark it executable
- install default templates into `~/.local/share/chronora/templates`
- warn if `~/bin` is not in `PATH`

## Quick Start

In any project directory:

```bash
cd ~/work/my-project
cclaude
```

On first run, the adapter creates:

- `.claude/current.md`
- `.claude/CLAUDE.local.md`
- `.claude/sessions/`
- `CLAUDE.local.md` symlink at the project root

Then the workflow becomes:

1. start the coding session
2. read the deterministic project state
3. do the work
4. update `current.md` when durable truth changes
5. let the append-only archive record the session

## Example Project

See `examples/project-example/` for a minimal reference layout.

The example demonstrates:

- a project-local `.claude/` state directory
- a root-level `CLAUDE.local.md` symlink
- a seeded `current.md`
- a placeholder session archive directory

## Multi-Agent Compatibility

This project is not conceptually tied to Claude.

It should be understood as an **AI IDE Continuity Layer**:

- Claude Code can be one frontend.
- Codex can be one frontend.
- OpenCode can be one frontend.
- IDE-native agents can be frontends.

Any agent that can reliably read, respect, and update the state contract can participate.

That matters because long-running software work will increasingly involve multiple agents across different interfaces. Shared deterministic state is what lets those agents coordinate without pretending they all share one perfect memory.

## Long-Term Vision

The long-term vision is an AI operating workspace for software projects.

That workspace should eventually support:

- summary compression across long time horizons
- explicit task graphs with dependency state
- multi-agent coordination over shared project state
- state validation and conflict detection
- project-level continuity independent of any single frontend
- an operating model where agents are replaceable but state remains stable

In that world, AI development infrastructure looks less like chat history management and more like a project state engine.

## Future Roadmap

Near- and mid-term directions include:

- first-class `tasks/` support for durable task continuity
- first-class `summaries/` support for structured compression layers
- additional frontend adapters beyond `cclaude`
- state linting and quality checks for `current.md`
- archive inspection and diff tooling
- multi-agent merge semantics for concurrent state updates
- workspace-level abstractions for AI operating environments

## Design Principles

1. **Determinism over recall** — exact state is more important than approximate retrieval.
2. **Local-first operation** — continuity should work without external infrastructure.
3. **Human readability** — state must stay understandable to engineers.
4. **Append-only history** — historical evidence should not be destroyed during iteration.
5. **Frontend neutrality** — the state model should outlive any single tool.
6. **Minimal hidden behavior** — core mechanisms should be inspectable in files and scripts.
7. **State compression with discipline** — summaries should reduce entropy, not create new ambiguity.

## FAQ

### Is this a Claude-only tool?

No. The current repository ships a Claude Code adapter as the reference implementation, but the architecture is frontend-agnostic. This project is best understood as an AI IDE continuity layer.

### Why not just rely on chat history?

Because chat history is implicit, token-bounded, and poor at separating old reasoning from current truth. Software continuity needs editable state.

### Why plain Markdown files instead of a database or vector store?

Because the primary requirement is determinism, inspectability, and low operational complexity. Plain files are easier to audit and correct.

### What belongs in `current.md`?

Only durable project truth: architecture choices, active blockers, important constraints, current direction, and next steps. Not raw transcripts.

### Is the session archive the source of truth?

No. The archive is append-only historical evidence. `current.md` is the live operational state.

### Can multiple agents share the same project state?

Yes. In fact, that is one of the main reasons to formalize continuity as state instead of chat memory.

### Does this replace issue trackers or formal project management?

No. It complements them by providing an AI-native continuity layer inside the working repository.

### Why does this feel more like infrastructure than a wrapper?

Because the wrapper is only the bootstrap surface. The real system is the state model: deterministic context, append-only archives, and explicit continuity for long-running coding agents.
