# Getting Started

This guide walks through the current Chronora v0.2 Core onboarding flow from scratch.

## 1. Clone the repository

```bash
git clone https://github.com/CookieAteMe/chronora.git
cd chronora
```

## 2. Install Chronora

Run the installer from the repository root:

```bash
./install.sh
```

The installer currently does three things:

- installs `cclaude`
- installs the Python `chronora` CLI
- installs default templates under your local data directory

After installation, you should be able to run:

```bash
chronora restore
```

without using `python3 -m chronora.cli restore`.

If your shell cannot find `chronora` immediately, follow the PATH instruction printed by `install.sh`, then reload your shell.

## 3. Initialize a project

Move into any project directory and run:

```bash
cclaude
```

On first run, Chronora initializes:

```text
.claude/
├── current.md
├── CLAUDE.local.md
└── sessions/
```

It also creates a root-level `CLAUDE.local.md` symlink.

## 4. Run `chronora restore`

From the project root:

```bash
chronora restore
```

The command computes a restore plan from the state files it finds.
It does not launch or control an AI agent.

## 5. Inspect the output

Typical output includes:

- detected Chronora state files
- restore loading order
- suggested files to read
- warnings when state is missing or degraded
- a recommended prompt you can paste into an agent session

Example shape:

```text
Chronora Restore Plan
=====================
Project Root: /path/to/project
State Directory: /path/to/project/.claude

Detected State
--------------
- current: /path/to/project/.claude/current.md (Canonical live truth)
- archive: /path/to/project/.claude/sessions/2026-05-28_09-00-00-99999 (Latest archive evidence fallback)

Restore Order
-------------
1. /path/to/project/.claude/current.md — Canonical live truth
2. /path/to/project/.claude/sessions/2026-05-28_09-00-00-99999 — Latest archive evidence fallback
```

## 6. Recommended development commands

```bash
make install
make test
make lint
```

## Troubleshooting

### `chronora: command not found`

Your Python user script directory may not be in `PATH` yet.
Use the export line printed by `./install.sh`, then reload your shell.

### `python3 -m pip` is unavailable

Install pip for your Python 3 environment and rerun `./install.sh`.

### `chronora restore` shows no state

Run `cclaude` in the target project first so Chronora can create `.claude/current.md` and `.claude/sessions/`.
