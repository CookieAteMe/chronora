# Philosophy

## Overview

Chronora treats AI coding continuity as a state management problem.

The core claim is simple: coding agents need deterministic state more than they need better probabilistic recall. Chat history is helpful, but it is not a reliable source of operational truth for long-running software projects.

## File-Driven State

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

- what the agent believed before the session
- what changed during the session
- what state was left behind afterward

The archive is not the source of truth. It is the record of how truth changed.

## Explicit State Over Probabilistic Recall

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

Vector memory is useful for large-scale fuzzy retrieval.

Chronora is solving a different problem.

For coding continuity, the system of record should be:

- deterministic rather than approximate
- directly editable rather than retrieval-ranked
- compact enough to review quickly
- grounded in current truth rather than historical similarity

That is why Chronora does not depend on embeddings, databases, or retrieval infrastructure in v0.1.

## Compression Without Confusing Truth

Long-running AI workflows eventually need compression.

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

### Stable scope

Chronora v0.1 deliberately remains a continuity layer. It does not try to become a full AI runtime platform.

## What This Means for v0.1

Chronora is serious developer tooling, but intentionally narrow.

The repository focuses on:

- project-local persistent workflow
- deterministic state via `.claude/current.md`
- project-local instructions via `.claude/CLAUDE.local.md`
- append-only session archives via `.claude/sessions/`
- a small wrapper that keeps the workflow reproducible

That is enough to make long-running coding sessions materially more stable without redesigning the runtime around heavier abstractions.
