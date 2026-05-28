# current.md Guide

## What `current.md` Is

`current.md` is the canonical mutable project state for Chronora.

Its job is not to store everything that happened. Its job is to store the small set of facts that the next coding session must load before doing meaningful work.

A good `current.md` is:

- explicit
- compact
- durable
- easy to edit
- grounded in current truth

## Default Structure

The default template contains five sections:

```md
# Current Project

## Project Status
## Architecture
## Active Problems
## Important Decisions
## Next Steps
```

Each section has a distinct purpose.

### Project Status

Summarize where the project stands right now.

Good examples:

- `Login flow MVP works locally. Registration is partially implemented.`
- `Docs refactor is complete. Release checklist is still open.`

Bad examples:

- a long narrative of everything discussed in the last session
- vague statements like `working on stuff`

### Architecture

Record the structure the next session must respect.

Good examples:

- `FastAPI backend with a single entry point in src/main.py.`
- `The current entrypoint installs templates into ~/.local/share/chronora/templates.`

Keep this focused on active architecture, not speculative future designs.

### Active Problems

List the blockers, risks, or known gaps that still matter.

Good examples:

- `No rate limiting on /login yet.`
- `Archive inspection is documented, but not surfaced by a dedicated command.`

If a problem is solved, remove it from this section.

### Important Decisions

Preserve decisions the next session would otherwise be tempted to re-litigate.

Good examples:

- `Keep auth logic in one module until the API stabilizes.`
- `Do not replace .claude/ with a new runtime directory in v0.1.`

This section is especially useful when a decision is non-obvious but still active.

### Next Steps

Make the next session concrete.

Good examples:

1. `Add email validation to registration.`
2. `Write a sample archive walkthrough in the docs.`

Prefer actionable items over broad aspirations.

## What Belongs Here

`current.md` should contain:

- the current project status
- active architecture constraints
- unresolved blockers
- decisions that still shape the work
- the next concrete handoff steps

## What Should Stay Out

Do not turn `current.md` into:

- a chat transcript
- a scratchpad for transient debugging output
- a copy of code that already lives elsewhere
- a historical journal of every idea that came up
- a todo list with no connection to live project state

Chronora already has an archive for history. `current.md` is for current truth.

## How to Keep It Lean

A healthy `current.md` is edited, not merely appended to.

That means:

- update entries when reality changes
- remove stale blockers after they are resolved
- replace vague notes with concrete statements
- keep each section focused on facts the next session needs

If the file keeps growing but never gets cleaned up, it stops being state and becomes residue.

## When to Update It

Update `current.md` when durable facts change.

Common triggers:

- the architecture changed in a way that matters later
- a blocker was discovered and remains unresolved
- a decision was made that should constrain future work
- the next handoff became clearer

Do not update it for every debugging step. Update it when the state of the project changed.

## Example

```md
# Current Project

## Project Status

Chronora v0.1 README and positioning refactor is in progress.

## Architecture

The project currently uses a Claude-first entrypoint around `.claude/`, while positioning the continuity model as AI-tool agnostic.

## Active Problems

No additional frontend adapters are implemented yet.

## Important Decisions

Do not redesign the runtime or rename `.claude/` in v0.1.

## Next Steps

1. Strengthen support docs around workflow continuity.
2. Keep implementation claims aligned with actual frontend support.
3. Expand adapters later without overstating compatibility.
```

## Related Docs

- [Workflow](workflow.md)
- [Session Archive](session-archive.md)
- [Philosophy](philosophy.md)
