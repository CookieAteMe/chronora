# Chronora

Persistent context and session continuity workflow for AI coding tools.

> Coding agents need deterministic state, not probabilistic recall.

[中文文档](README.zh-CN.md) · [Workflow](docs/workflow.md) · [Philosophy](docs/philosophy.md) · [Example](examples/basic-project/README.md)

Chronora is v0.1 infrastructure for long-running coding sessions.

It gives AI coding tools a deterministic continuity layer built from ordinary project files: a canonical `current.md`, project-local agent instructions, and an append-only session archive. The goal is not to create a smarter chat wrapper. The goal is to make project state explicit, inspectable, editable, and durable.

## Why Chronora

Chat history is useful as execution trace, but it is a poor system of record for software work.

In short-lived tasks, conversational context is often enough. In real repositories, it breaks down quickly:

- architectural decisions get re-litigated every session
- unresolved blockers disappear into token history
- partially completed work gets rediscovered instead of resumed
- current truth and historical reasoning blur together
- the user becomes the only reliable memory system in the loop

Chronora addresses that by moving continuity out of hidden chat recall and into deterministic project state.

For coding agents, that means:

- **explicit project state** instead of inferred context
- **`current.md` continuity** instead of prompt-by-prompt reconstruction
- **append-only session history** that preserves how state changed over time
- **summary-friendly state** without treating raw transcripts as source of truth
- **deterministic continuity** across long-running coding sessions

## What Chronora Provides

Chronora keeps the runtime small on purpose. The v0.1 repository ships a focused workflow layer:

- `current.md` as the canonical mutable project state
- `CLAUDE.local.md` as project-local agent instructions
- `.claude/sessions/` as an append-only session archive
- `cclaude` as a bootstrap wrapper for Claude Code
- templates and examples that make the workflow reproducible

The current implementation is intentionally file-driven and shell-based. It does not introduce databases, vector stores, embeddings, or runtime orchestration layers.

## Installation

Chronora v0.1 is currently tested for **macOS with zsh** and requires the [Claude Code CLI](https://claude.ai/code).

```bash
git clone https://github.com/CookieAteMe/chronora.git
cd chronora
./install.sh
```

The installer:

- copies `cclaude` to `~/bin`
- installs default templates to `~/.local/share/chronora/templates`
- ensures the installed wrapper is executable
- checks whether the Claude Code CLI is available
- warns if `~/bin` is not currently in `PATH`

If needed, add this to `~/.zshrc` and reload your shell:

```bash
export PATH="$HOME/bin:$PATH"
```

## Usage

### 1. Initialize a project

Run `cclaude` from any project root:

```bash
cd ~/work/my-project
cclaude
```

On first run, Chronora creates:

```text
my-project/
├── .claude/
│   ├── current.md
│   ├── CLAUDE.local.md
│   └── sessions/
└── CLAUDE.local.md -> .claude/CLAUDE.local.md
```

### 2. Start a continuity-aware coding session

`cclaude` bootstraps the local state, snapshots the before-state, and launches Claude Code in the project context.

The expected session loop is:

1. run `cclaude`
2. load `.claude/current.md`
3. continue the existing architecture and constraints
4. update `current.md` when durable facts change
5. exit and let Chronora archive the session

### 3. Use `current.md` as live project truth

A healthy `current.md` stays compact and operational. It records the facts the next session must treat as true now:

```md
# Current Project

## Project Status

Login flow MVP is working locally. Registration is partially implemented.

## Architecture

FastAPI backend with a single entry point in `src/main.py`.

## Active Problems

No rate limiting on `/login` yet.

## Important Decisions

Keep auth logic in one module until the API stabilizes.

## Next Steps

1. Add email validation to registration.
2. Add integration coverage for happy-path login.
```

### 4. Inspect the session archive

Every run creates an append-only archive under `.claude/sessions/`.

A typical archive directory contains:

```text
.claude/sessions/2026-05-27_10-00-00-12345/
├── current.before.md
├── current.after.md
├── CLAUDE.local.before.md
├── CLAUDE.local.after.md
└── session.meta
```

This gives you a lightweight history of how project state evolved without turning chat transcripts into the primary state system.

### 5. Resume later without reconstructing context

The next day, or in the next terminal, run:

```bash
cclaude
```

Chronora resumes from explicit state instead of hoping the model remembers the right architectural context from prior conversation history.

## Project Structure

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
│   ├── current-md-guide.md
│   ├── migration.md
│   ├── philosophy.md
│   ├── session-archive.md
│   └── workflow.md
└── examples/
    ├── basic-project/
    └── project-example/
```

### State layout inside a target project

```text
your-project/
├── .claude/
│   ├── current.md
│   ├── CLAUDE.local.md
│   └── sessions/
└── CLAUDE.local.md -> .claude/CLAUDE.local.md
```

## Docs

- [Workflow](docs/workflow.md) — how the session lifecycle works in practice
- [current.md Guide](docs/current-md-guide.md) — what belongs in the canonical state file
- [Session Archive](docs/session-archive.md) — how to read the append-only archive
- [Philosophy](docs/philosophy.md) — the design rationale behind deterministic state
- [Architecture](docs/architecture.md) — component overview and failure model
- [Migration Guide](docs/migration.md) — how to move from an ad hoc workflow

## Examples

- [examples/basic-project/](examples/basic-project/README.md) — a realistic v0.1 onboarding example with populated state and a sample archive
- [examples/project-example/](examples/project-example/README.md) — the minimal structural example

## Current Scope

Chronora is intentionally narrow in v0.1.

It is currently:

- persistent workflow infrastructure for Claude Code users
- a deterministic state layer for long-running coding sessions
- a file-based continuity mechanism built around `.claude/`
- a serious shell workflow, not a full runtime platform

It is not yet:

- a database-backed state engine
- a vector-memory product
- a multi-agent orchestrator
- a generalized runtime for every coding frontend

## Why Deterministic State Matters

Chronora treats project continuity as a state management problem.

That means the system distinguishes clearly between:

- **history** — what happened
- **current state** — what is true now
- **future work** — what the next session should pick up

This boundary is what makes long-running coding sessions stable. History remains valuable, but it does not replace source-of-truth state.

## Roadmap

Near-term directions for Chronora include:

- better onboarding for new repositories
- stronger `current.md` guidance and examples
- better archive inspection ergonomics
- more examples for different project shapes
- additional adapters beyond the current Claude Code reference workflow
- future-compatible state domains for summaries and task continuity

## License

Chronora is released under the [MIT License](LICENSE).
