# Architecture

## Overview

Stateful AI Workflow is a file-based wrapper around Claude Code.

The system has one goal: preserve durable project context across sessions without relying on hidden chat history or external retrieval systems.

## Components

### 1. `bin/cclaude`

The wrapper entrypoint.

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

It teaches Claude to read and maintain `.claude/current.md` as durable state.

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

The wrapper should stay understandable in a single read. The entire mechanism should be maintainable with shell scripts and Markdown.

### Non-invasive integration

The wrapper must not rewrite or depend on the main `CLAUDE.md` in the target project.

### Local-first operation

Everything should work with local files only. No indexing service, database, or embedding store is required.

## Data Flow

1. User runs `cclaude` in a project.
2. Wrapper initializes `.claude/` state files if missing.
3. Wrapper archives the starting state.
4. Claude session runs.
5. User or Claude updates `.claude/current.md` as decisions evolve.
6. Wrapper archives the ending state on exit.
7. Next session resumes from the saved state.

## Failure Model

The system is deliberately simple:

- if a template is missing, initialization fails loudly
- if the root `CLAUDE.local.md` already exists as a real file, the wrapper does not overwrite it
- if Claude CLI is missing, the wrapper exits with a clear message

This avoids silent mutation of project files.
