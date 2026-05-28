# Example Project

This example shows how a target repository looks after running `cclaude`.

## Layout

```text
project-example/
├── .claude/
│   ├── current.md
│   ├── CLAUDE.local.md
│   └── sessions/
├── CLAUDE.local.md -> .claude/CLAUDE.local.md
└── src/
    └── app.txt
```

The key idea is that durable Claude state lives inside `.claude/`, while the root symlink makes the local instructions easy to discover.
