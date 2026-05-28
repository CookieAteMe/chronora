# Stateful AI Workflow

A lightweight wrapper around Claude Code that turns short-lived chat sessions into a stateful, file-based workflow.

Instead of relying on the model to remember everything from prior conversations, this project stores durable project context in plain Markdown files inside `.claude/`. Each new Claude session starts by reading the current project state, continues the same architecture and decisions, and writes back any important updates before ending.

## Why Persistent AI Context Matters

Most AI coding workflows are still chat-driven. They work well for isolated tasks, but they degrade when a project spans many sessions, architectural decisions, and unfinished branches of work.

The usual failure modes are simple:

- the model forgets earlier constraints
- the same architecture gets re-litigated every session
- partially solved problems are rediscovered from scratch
- the user becomes the only source of continuity

Persistent AI context fixes that by moving continuity out of the chat log and into explicit project state.

## State-Driven AI vs Chat-Driven AI

| Approach | Source of continuity | Failure mode | Operational model |
| --- | --- | --- | --- |
| Chat-driven AI | Conversation history | Context drift, repetition, hidden assumptions | Ask again every session |
| State-driven AI | Files such as `.claude/current.md` | State quality depends on disciplined updates | Read state, act, update state |

State-driven AI treats the AI more like a collaborator joining an ongoing project, not like a chatbot starting from zero.

## Architecture Design

The wrapper is intentionally small.

```text
stateful-ai-workflow/
├── README.md
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

Runtime behavior inside a target project:

```text
your-project/
├── .claude/
│   ├── current.md
│   ├── CLAUDE.local.md
│   └── sessions/
└── CLAUDE.local.md -> .claude/CLAUDE.local.md
```

Core ideas:

- `bin/cclaude` is the entrypoint.
- `.claude/current.md` stores durable project state.
- `.claude/CLAUDE.local.md` stores Claude-specific workflow rules for the project.
- `CLAUDE.local.md` at the root is only a symlink for convenience.
- `.claude/sessions/` stores session snapshots before and after each run.

The wrapper never edits the project's main `CLAUDE.md`.

## Workflow

1. Run `cclaude` from a project root.
2. The wrapper creates `.claude/` if needed.
3. The wrapper creates `current.md` and `CLAUDE.local.md` from templates if they do not exist.
4. The wrapper creates a root symlink: `CLAUDE.local.md -> .claude/CLAUDE.local.md`.
5. The wrapper archives the session state into `.claude/sessions/<timestamp>/`.
6. Claude starts with the project state already present.
7. During important discussions or implementation steps, update `.claude/current.md`.
8. The next session resumes from the updated state instead of from memory alone.

See `docs/workflow.md` for a fuller walkthrough.

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd stateful-ai-workflow
```

### 2. Install the wrapper

```bash
./install.sh
```

The installer:

- copies `cclaude` to `~/bin`
- makes it executable
- installs the templates into the user data directory
- checks whether `~/bin` is in `PATH`

## Usage Example

Inside any project:

```bash
cd ~/work/my-project
cclaude
```

On first run, the wrapper will create:

- `.claude/current.md`
- `.claude/CLAUDE.local.md`
- `.claude/sessions/`
- `CLAUDE.local.md` symlink at the project root

Typical loop:

1. Start a Claude session with `cclaude`.
2. Let Claude read `.claude/current.md` before making decisions.
3. When architecture, blockers, or next steps change, update `current.md`.
4. End the session.
5. Start the next session with the same state already available.

A complete example project lives in `examples/project-example/`.

## Session Archive Mechanism

Every `cclaude` run creates a timestamped archive directory under `.claude/sessions/`.

Each archive stores:

- session metadata
- the starting `current.md`
- the starting `CLAUDE.local.md`
- the ending `current.md`
- the ending `CLAUDE.local.md`
- the wrapper exit code

This gives you a lightweight audit trail of how project state changed across sessions without requiring a database or external memory service.

## The Role of `current.md`

`current.md` is the durable working memory for the project.

It should contain only information that remains valuable across sessions, such as:

- current project goal
- stable architecture choices
- active constraints
- unresolved problems
- next planned steps

It should not become a raw conversation transcript. The file is most useful when it stays concise, editable, and intentionally stateful.

## Why Not Vector Memory

This project does not use embeddings or vector retrieval for project continuity.

That is a deliberate choice.

For project-state continuity, plain files have major advantages:

- they are explicit and inspectable
- they are easy to edit by hand
- they fail deterministically instead of silently missing retrieval
- they work offline
- they do not require indexing, chunking, or ranking infrastructure
- they map cleanly to how engineers already reason about project state

Vector memory is useful for large, fuzzy knowledge retrieval. It is less useful when the goal is to preserve a compact, shared, continuously edited project state.

## Repository Contents

- `bin/cclaude` — the runtime wrapper
- `templates/` — default files generated into projects
- `docs/architecture.md` — system design and component responsibilities
- `docs/workflow.md` — day-to-day operating model
- `docs/migration.md` — how to migrate from an existing wrapper or ad hoc setup
- `examples/project-example/` — sample target project layout

## License

This repository is released under the MIT License.
