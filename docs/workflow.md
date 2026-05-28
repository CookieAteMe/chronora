# Workflow

## Goal

Use Chronora to keep project state explicit across long-running AI coding sessions.

This workflow is intentionally simple:

1. start from explicit project state
2. do the work inside that state
3. update only durable facts
4. archive the session without mutating history
5. resume later from the updated state

## Prerequisites

Chronora v0.1 currently assumes:

- macOS with zsh
- Claude Code CLI installed
- `cclaude` installed via `./install.sh`

Claude Code is the only fully supported coding frontend today.

## First Run

From any project root:

```bash
cclaude
```

Chronora initializes:

- `.claude/current.md`
- `.claude/CLAUDE.local.md`
- `.claude/sessions/`
- `CLAUDE.local.md` symlink in the project root

The entrypoint then snapshots the before-state and launches Claude Code in the same project.

## Session Lifecycle

```text
run cclaude
  -> ensure local state files exist
  -> snapshot before-state
  -> run Claude Code in project context
  -> update current.md if durable facts changed
  -> snapshot after-state
  -> append archive metadata
```

Chronora is deliberately conservative here. The goal is workflow continuity, not hidden automation.

## Recommended Operating Loop

### 1. Start from state

At the beginning of each session:

- run `cclaude`
- read `.claude/current.md`
- understand the current architecture, active problems, and next steps before changing code

### 2. Work within the existing context

During the session:

- make code or documentation changes
- preserve existing technical decisions unless they truly changed
- avoid treating the chat transcript as the only source of truth

### 3. Update `current.md` when durable truth changes

A good update to `current.md` records state that the next session must load immediately.

Typical updates include:

- architecture decisions that affect future work
- blockers that remain unresolved after the session
- partial implementation state that must be resumed later
- concrete next steps for the next session

## What Belongs in `current.md`

| Good state | Why it belongs |
| --- | --- |
| project status | tells the next session where the work stands |
| architecture decisions | prevents re-litigating key structure |
| active blockers | keeps real constraints visible |
| important decisions | preserves rationale that still matters |
| next steps | makes resumption concrete |

## What Does Not Belong in `current.md`

| Bad content | Why it should stay out |
| --- | --- |
| casual conversation | not durable project state |
| verbose logs | high-noise, low-value state |
| transient debugging output | expires quickly and clutters the file |
| duplicated source code | the repository already stores code truth |
| raw transcript excerpts | history is not live operational state |

## Archive Role in the Workflow

When the agent exits, Chronora writes a before/after archive for the session.

That archive answers:

- what the project state was before the run
- what changed during the run
- what the project state looked like when the run ended

The archive is history.

`current.md` is still the live source of truth.

## Recovering from a Bad Session

If a session leaves `current.md` in the wrong shape:

1. inspect the most recent directory under `.claude/sessions/`
2. compare `current.before.md` and `current.after.md`
3. restore the correct facts by editing live `current.md`
4. keep the archive intact as historical evidence

Chronora does not treat archive history as mutable truth. It preserves evidence and lets the live state be corrected explicitly.

## Team Usage

Chronora also works in shared repositories when a team agrees that `.claude/current.md` is a state document, not a conversation dump.

That requires editorial discipline:

- keep the file small
- remove stale items quickly
- prefer concrete facts over speculative notes
- update the state when project reality changes

## Related Docs

- [current.md Guide](current-md-guide.md)
- [Session Archive](session-archive.md)
- [Philosophy](philosophy.md)
- [Migration Guide](migration.md)
