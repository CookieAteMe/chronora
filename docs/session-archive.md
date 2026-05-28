# Session Archive

## Overview

Chronora records an append-only archive for each `cclaude` run.

The archive exists to preserve how project state changed over time. It is not the live source of truth. That role still belongs to `.claude/current.md`.

## Archive Structure

Each session creates a timestamped directory under `.claude/sessions/`.

A typical archive looks like this:

```text
.claude/sessions/2026-05-27_10-00-00-12345/
├── current.before.md
├── current.after.md
├── CLAUDE.local.before.md
├── CLAUDE.local.after.md
└── session.meta
```

## File Meanings

### `current.before.md`

A snapshot of the live `current.md` before Claude Code starts.

### `current.after.md`

A snapshot of the live `current.md` after the session ends.

### `CLAUDE.local.before.md`

A snapshot of the project-local agent instructions before the session.

### `CLAUDE.local.after.md`

A snapshot of the project-local agent instructions after the session.

### `session.meta`

Basic metadata about the run.

The current wrapper writes:

- `started_at`
- `ended_at`
- `project_root`
- `claude_dir`
- `exit_code`

## How to Read an Archive

An archive answers a small set of practical questions:

- what state did the session start from
- what state did the session end with
- did the local instructions change
- did the session exit cleanly

A common inspection pattern is:

```bash
diff -u .claude/sessions/<session>/current.before.md \
  .claude/sessions/<session>/current.after.md
```

That gives you a direct view of what durable project state changed during that run.

## History vs Live State

Chronora keeps a strong distinction between:

- **archive history** — what happened during earlier runs
- **live state** — what the project should treat as true right now

If the live `current.md` is wrong, correct the live file directly.

Do not treat archive history as mutable truth.

## Generated Transcript Files

Some Claude Code environments may also generate `*.typescript` transcript capture artifacts during sessions.

These files are runtime noise from the perspective of Chronora’s source repository. They should not be treated as the canonical archive format, and they are ignored by the repository’s `.gitignore` rules.

## Runtime Archives vs Tracked Example Archives

In a real project, `.claude/sessions/` is runtime output.

In this repository, the root project’s runtime archives are ignored. Example directories may include tracked sample archives so readers can inspect the format without generating one themselves.

This distinction is intentional:

- runtime archives are local workflow artifacts
- example archives are documentation by example

## Cleanup and Retention

Chronora v0.1 does not implement archive rotation.

If your local session history grows too large, you can prune old archives manually in the target project. That cleanup should be a user decision, not an automatic mutation by the wrapper.

## Related Docs

- [Workflow](workflow.md)
- [current.md Guide](current-md-guide.md)
- [Philosophy](philosophy.md)
