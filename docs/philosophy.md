# Philosophy

## Overview

Chronora treats AI coding continuity as a state management problem.

The central claim is simple: coding agents need deterministic state more than they need better probabilistic recall. Chat history is useful as execution trace, but it is not a reliable source of operational truth for long-running software work.

## Why Explicit State Matters

Project state and chat history are not interchangeable.

In short sessions, transcript memory may be enough. In real repositories, repeated agent sessions introduce drift:

- current architectural constraints get buried in prior messages
- unresolved blockers vanish into old context windows
- partially completed work gets rediscovered instead of resumed
- historical reasoning gets mistaken for live truth

Chronora answers that with explicit, editable state files.

## File-Driven Continuity

Chronora keeps critical context in ordinary project files.

That matters because files are:

- visible to humans and tools
- editable when reality changes
- versionable with normal source control
- inspectable without proprietary infrastructure

This is why `current.md` exists as a canonical mutable state file rather than as a hidden tool-managed memory store.

## Append-Only History

Chronora treats session archives as historical evidence.

Every run captures before/after state so the project can preserve:

- what the agent started from
- what changed during the session
- what state was left behind afterward

The archive is not the source of truth. It is the record of how truth changed.

## Deterministic Continuity Over Probabilistic Recall

In real software projects, the important questions are usually not:

- which previous conversation chunk is most similar
- which historical sentence ranks highest in retrieval
- whether the model happens to remember the right constraint this time

The important questions are:

- what is the current architecture decision
- what is actually blocked right now
- what should the next session treat as true
- what should the next session do next

Those are state questions.

Chronora answers them with explicit files rather than probabilistic recall.

## Why Not Vector Memory

Vector memory is useful for fuzzy retrieval across large information sets.

Chronora is solving a different problem.

For coding workflow continuity, the system of record should be:

- deterministic rather than approximate
- directly editable rather than retrieval-ranked
- compact enough to review quickly
- grounded in current truth rather than historical similarity

That is why Chronora does not depend on embeddings, databases, or retrieval infrastructure in v0.1.

## Compression Without Confusing Truth

Long-running AI coding workflows eventually need compression.

Chronora draws a hard boundary between:

- **history** — what happened
- **current state** — what is true now
- **future summaries** — compressed views built from history and state

The archive is append-only history.

`current.md` is live truth.

This boundary prevents the common failure mode where old reasoning is mistaken for current fact.

## Design Principles

### Determinism over recall

Exact, inspectable state matters more than approximate memory retrieval.

### Local-first operation

The continuity mechanism should work with ordinary local files and shell scripts.

### Human readability

Engineers should be able to open the state directly, understand it, and fix it.

### Append-only history

Historical evidence should accumulate rather than be overwritten.

### Minimal hidden behavior

The workflow should be understandable from the repository, not from invisible runtime magic.

### Claude-first, tool-agnostic architecture

The first complete implementation path is Claude Code, but the continuity model is not conceptually limited to one coding agent.

## What This Means for v0.1

Chronora is infrastructure for AI coding workflows, but intentionally narrow.

The repository currently focuses on:

- persistent project context
- deterministic state via `.claude/current.md`
- project-local instructions via `.claude/CLAUDE.local.md`
- append-only session history via `.claude/sessions/`
- a Claude-first entrypoint that keeps the workflow reproducible

Planned integrations with other coding tools belong to the roadmap, not the current compatibility matrix.
