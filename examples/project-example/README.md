# Example Project

This example shows the smallest useful Chronora layout.

It is intentionally minimal and exists to demonstrate the shape of a target project after `cclaude` bootstraps local state.

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

This example is useful when you only want to inspect the directory structure.

For a more realistic walkthrough with populated project state and a sample archive, see [examples/basic-project/](../basic-project/README.md).
