# Workflow

## Goal

Use Claude across many sessions without losing architectural continuity.

## First-Time Setup

1. Install the wrapper with `./install.sh`.
2. Add `~/bin` to `PATH` if needed.
3. Open any project directory.
4. Run `cclaude`.

## What Happens on First Run

The wrapper creates:

- `.claude/current.md`
- `.claude/CLAUDE.local.md`
- `.claude/sessions/`
- `CLAUDE.local.md` symlink in the project root

At that point the project has persistent Claude state without changing its main `CLAUDE.md`.

## Recommended Operating Loop

### Start

At the beginning of each session:

- run `cclaude`
- read `.claude/current.md`
- understand the architecture, open issues, and next steps before changing code

### Work

During the session:

- make code or documentation changes
- keep architecture consistent with existing decisions
- avoid treating the chat transcript as the only source of truth

### Update State

After meaningful progress:

- update `.claude/current.md`
- keep only durable information
- remove stale items when they are no longer relevant

Good things to store:

- decisions that affect future implementation
- unresolved blockers
- partial work that another session must continue
- next concrete action

Bad things to store:

- casual conversation
- verbose logs
- transient debugging output
- duplicated content from other source files

### End

When Claude exits, the wrapper saves a before/after archive for the session.

## Team Usage

This workflow also works in shared repositories when teams agree to treat `.claude/current.md` as a state document instead of a conversation dump.

The important discipline is editorial, not technical: keep the file small, current, and durable.
