# Chronora

Persistent context and continuity workflow for AI coding tools.

> Coding agents need deterministic state, not probabilistic recall.

[中文文档](README.zh-CN.md) · [Workflow](docs/workflow.md) · [Philosophy](docs/philosophy.md) · [Architecture](docs/architecture.md) · [Example](examples/basic-project/README.md)

Chronora is a Claude-first continuity layer for long-running AI coding workflows.

It keeps persistent project context in ordinary files so coding agents can resume work from explicit state instead of reconstructing context from chat history. The architecture is AI-tool agnostic; the current v0.1 implementation is fully wired for Claude Code.

## Why Chronora

Chat history is not the same thing as project state.

In real development workflows, long-running sessions drift:

- architecture decisions get re-litigated
- unresolved blockers disappear into transcript history
- partial implementations get rediscovered instead of resumed
- current truth gets mixed with old reasoning
- the human operator becomes the only dependable memory layer

Chronora treats continuity as a deterministic state problem:

- **explicit state** for what is true now
- **append-only history** for what changed
- **compact handoff structure** for what the next session should do
- **workflow continuity** that survives context-window churn

Deterministic continuity is more reliable than probabilistic recall when the work spans days, branches, and repeated agent sessions.

## What Chronora Provides

Chronora v0.1 ships a deliberately small continuity layer:

- `current.md` as canonical mutable project state
- `CLAUDE.local.md` as project-local agent instructions
- `.claude/sessions/` as append-only state history
- `cclaude` as the current Claude Code entrypoint
- templates and examples that make the workflow reproducible

The implementation is intentionally file-driven and shell-based. It does not depend on databases, embeddings, vector memory, or a hidden orchestration service.

## Support Status

Current support:

- Claude Code (fully supported)

Planned integrations:

- Codex CLI
- OpenCode
- Aider
- Cursor agents

These planned integrations are not shipped in v0.1. Chronora is Claude-first in implementation today, while keeping the continuity model general enough to extend beyond a single coding agent later.

## Installation

Chronora v0.1 is currently tested for **macOS with zsh** and requires the [Claude Code CLI](https://claude.ai/code).

```bash
git clone https://github.com/CookieAteMe/chronora.git
cd chronora
./install.sh
```

The installer:

- copies `cclaude` to the first supported directory already on `PATH` (`~/.local/bin`, otherwise `~/bin`)
- installs default templates to `~/.local/share/chronora/templates`
- ensures the installed entrypoint is executable
- checks whether the Claude Code CLI is available
- warns if the chosen install directory is not currently in `PATH`

If needed, add the suggested line from the installer output to `~/.zprofile` or `~/.zshrc`, then reload your shell:

```bash
export PATH="$HOME/.local/bin:$PATH"
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

This is the only fully supported frontend path today.

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

The current on-disk layout is Claude-first, but the continuity model is meant to outlast a single frontend.

## Docs

- [Workflow](docs/workflow.md) — the operating loop for long-running AI coding workflows
- [current.md Guide](docs/current-md-guide.md) — what belongs in live project state
- [Session Archive](docs/session-archive.md) — how to inspect append-only state history
- [Philosophy](docs/philosophy.md) — why deterministic state beats probabilistic recall
- [Architecture](docs/architecture.md) — continuity primitives, Claude-first entrypoint, and failure model
- [Migration Guide](docs/migration.md) — how to move from ad hoc AI coding workflows

## Examples

- [examples/basic-project/](examples/basic-project/README.md) — a realistic v0.1 onboarding example with populated state and a sample archive
- [examples/project-example/](examples/project-example/README.md) — the minimal structural example

## Current Scope

Chronora is intentionally narrow in v0.1.

It is currently:

- AI coding workflow continuity infrastructure
- deterministic state for long-running development
- Claude-first in implementation
- AI-tool agnostic in architecture
- local, file-based, and inspectable by default

It is not yet:

- multi-frontend runtime support
- a shipped summary layer
- task orchestration across agents
- a unified runtime for every coding tool
- full AI workspace orchestration

## Roadmap

Near-term directions for Chronora include:

- summary layer
- task continuity
- multi-agent adapters
- unified runtime layer
- AI workspace orchestration

These roadmap items describe the direction of the project, not features already available in v0.1. The current production path remains Claude Code.

## License

Chronora is released under the [MIT License](LICENSE).
