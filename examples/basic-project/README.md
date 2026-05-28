# Basic Project Example

This example shows a more realistic Chronora v0.1 workflow.

It demonstrates:

- a populated `.claude/current.md`
- project-local agent instructions in `.claude/CLAUDE.local.md`
- a root `CLAUDE.local.md` symlink
- a tracked sample session archive
- a tiny source tree with enough context to feel like a real project

## What this example represents

Imagine a small API project that already has one working login flow and is being continued across sessions.

The important point is not the application itself. The important point is how project truth is preserved in files that the next session can read immediately.

## Layout

```text
basic-project/
├── .claude/
│   ├── current.md
│   ├── CLAUDE.local.md
│   └── sessions/
│       └── 2026-05-27_10-00-00-12345/
│           ├── current.before.md
│           ├── current.after.md
│           ├── CLAUDE.local.before.md
│           ├── CLAUDE.local.after.md
│           └── session.meta
├── CLAUDE.local.md -> .claude/CLAUDE.local.md
└── src/
    └── main.py
```

## How to read it

1. Start with `.claude/current.md` to see the current live project state.
2. Read `.claude/sessions/2026-05-27_10-00-00-12345/` to see how one session changed that state.
3. Inspect `src/main.py` to understand the tiny project context the state file is describing.

This example is documentation by example. It exists to make the workflow inspectable without requiring you to generate your own session archive first.
