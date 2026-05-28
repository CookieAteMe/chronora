# Migration Guide

## Who This Is For

Use this guide if you already have:

- an ad hoc AI coding workflow launcher
- a manually maintained `CLAUDE.local.md`
- project notes stored in random chat transcripts
- a memory process without a stable archive structure

## Migration Strategy

The goal is not to preserve every historical conversation. The goal is to preserve the durable state that future sessions still need.

## Step 1: Install the Current Entrypoint

Install `cclaude` with:

```bash
./install.sh
```

## Step 2: Create `.claude/current.md`

Start from `templates/current.md` and copy only the information that still matters:

- active project status
- architecture decisions
- known problems
- next planned steps

Do not migrate full transcripts.

## Step 3: Move Project-Local Rules

If you already have local Claude-first instructions, merge them into `.claude/CLAUDE.local.md`.

Keep the instructions focused on durable workflow behavior, especially the requirement to read and update `current.md`.

## Step 4: Preserve Main `CLAUDE.md`

Do not move project-wide shared instructions unless you mean to change them.

The current entrypoint is designed to coexist with a repository's normal `CLAUDE.md` without editing it.

## Step 5: Standardize Session Archives

After migration, use `.claude/sessions/` as the only archive location for Chronora-managed session state.

This makes historical state changes easy to inspect and compare.

## Suggested Cleanup

After the migration:

- remove duplicate note files
- stop storing long-lived context only in chat logs
- stop editing multiple competing state files

## Migration Checklist

- [ ] `cclaude` installed in `~/bin`
- [ ] `.claude/current.md` exists
- [ ] `.claude/CLAUDE.local.md` exists
- [ ] `CLAUDE.local.md` symlink exists at the root
- [ ] `.claude/sessions/` exists
- [ ] durable project state copied into `current.md`
- [ ] obsolete launcher-specific notes removed
