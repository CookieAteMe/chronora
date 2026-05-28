# Architecture

## Overview

Chronora is a file-based continuity layer for AI coding workflows.

Its current implementation is Claude-first, with Claude Code as the only fully supported frontend in v0.1. The broader architecture is intentionally tool-agnostic: preserve durable project context across sessions without depending on hidden chat history or external retrieval systems.

## Components

### 1. `bin/cclaude`

The current entrypoint.

Responsibilities:

- detect the current project root from the shell working directory
- create `.claude/` and `.claude/sessions/` when missing
- materialize `current.md` and `CLAUDE.local.md` from templates
- create a convenience symlink at the project root
- snapshot session state before Claude starts
- snapshot session state again when Claude exits
- preserve the project's main `CLAUDE.md`

### 2. `templates/current.md`

The default state file for new projects.

It is intentionally small so users can adapt it to the project rather than inherit a rigid schema.

### 3. `templates/CLAUDE.local.md`

The default project-local instruction file.

It teaches the current Claude-first workflow to read and maintain `.claude/current.md` as durable state.

### 4. `.claude/current.md`

The canonical project state file.

This is the human-editable source of truth for long-lived context such as:

- project status
- architecture decisions
- blockers
- next steps

### 5. `.claude/sessions/`

An append-only session archive.

Each run stores a before/after snapshot and basic metadata. This keeps the workflow inspectable and debuggable.

## Design Principles

### Plain files over hidden memory

All important state should be visible, editable, and versionable.

### Small surface area

The implementation should stay understandable in a single read. The entire mechanism should be maintainable with shell scripts and Markdown.

### Non-invasive integration

The current entrypoint must not rewrite or depend on the main `CLAUDE.md` in the target project.

### Local-first operation

Everything should work with local files only. No indexing service, database, or embedding store is required.

### Claude-first, adapter-ready scope

The current runtime path is built around Claude Code, but the continuity primitives are meant to support future adapters rather than lock the project into a Claude-exclusive identity.

## Data Flow

1. User runs `cclaude` in a project.
2. Chronora initializes `.claude/` state files if missing.
3. Chronora archives the starting state.
4. Claude Code session runs.
5. User or agent updates `.claude/current.md` as decisions evolve.
6. Chronora archives the ending state on exit.
7. Next session resumes from the saved state.

## Failure Model

The system is deliberately simple:

- if a template is missing, initialization fails loudly
- if the root `CLAUDE.local.md` already exists as a real file, the entrypoint does not overwrite it
- if Claude Code CLI is missing, the entrypoint exits with a clear message

This avoids silent mutation of project files.
