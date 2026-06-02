# Chronora Summary Layer Specification

## Overview

Chronora needs a compression layer between **append-only session history** and **current operational state**.

That layer is the **Summary Layer**.

Its job is to take long conversations, long development processes, and growing session archives, then preserve only the parts that still matter for future continuity.

The Summary Layer exists so that a project can remain understandable and maintainable over time without forcing every future session to reread raw history.

It is not a replacement for canonical state.
It is a derived historical layer that helps carry durable meaning forward.

---

## 1. Responsibilities of the Summary Layer

The Summary Layer should perform six core responsibilities.

### 1.1 Compress historical evidence into maintainable continuity artifacts

Session archives are append-only evidence.
The Summary Layer condenses them into smaller, more reusable continuity documents.

### 1.2 Preserve durable meaning rather than raw chronology

The goal is not to replay everything that happened.
The goal is to preserve the information that still affects future work.

### 1.3 Reduce repeated rereading cost

Without summaries, every long-running project eventually forces new sessions to inspect too much archive history.
The Summary Layer reduces that cost.

### 1.4 Support long-horizon continuity

A project that spans many sessions, days, or weeks needs a way to carry forward decisions, changes, and unresolved work without depending on transcript memory.

### 1.5 Support restore and reconstruction workflows

When live state drifts, summaries provide compressed historical context before falling back to raw archives.

### 1.6 Support token compression

Summaries reduce the amount of history that must be reloaded into context.
They provide a deterministic, file-based alternative to rereading long transcripts or archives.

## 1.7 What the Summary Layer is not

The Summary Layer is **not**:

- the canonical source of truth
- a replacement for `current.md`
- a replacement for `tasks.md`
- a replacement for `handoff.md`
- a full transcript archive
- a dump of everything that happened

Summaries exist to preserve **what still matters**, not **everything that ever happened**.

---

## 2. Session → Summary Transformation Rules

A summary should be produced by transforming raw session history into durable continuity information.

## 2.1 Input

The inputs to summary creation are:

- session archives
- current canonical state
- current task state
- current handoff state
- any already-existing lower-level summaries when rolling up history

## 2.2 Output

The output is a compressed historical artifact that explains:

- what changed
- what decisions matter
- what remains unresolved
- what future sessions should still remember
- what can now be safely ignored

## 2.3 Transformation rule

The transformation rule is:

> Preserve durable continuity value. Discard transient execution detail.

A summary should prefer:

- meaning over chronology
- outcomes over narration
- constraints over chatter
- decisions over exploration
- unresolved issues over temporary detours

## 2.4 Preserve rules

A summary should preserve information that still has continuity value.

### Preserve these classes of information

- architecture changes that still define the project
- durable decisions that constrain future work
- corrections to earlier false assumptions
- active blockers that remain unresolved
- important status transitions that matter beyond one session
- rationale required to prevent re-litigating a key decision
- milestone progress that changes how the project should be understood
- deferred issues that still deserve future attention
- references to important files, areas, or milestones when they help future navigation

## 2.5 Discard rules

A summary should intentionally discard information that no longer adds continuity value.

### Discard these classes of information

- raw transcript detail
- repeated exploration that did not change the outcome
- tactical chatter and conversational filler
- verbose debugging logs
- disproven hypotheses that left no durable lesson
- dead-end implementation ideas that no longer matter
- step-by-step chronology when only the end-state matters
- redundant detail already absorbed into `current.md`, `tasks.md`, or `handoff.md`
- temporary runtime noise without ongoing project significance

## 2.6 Compression test

A useful summary should pass this test:

> If a future session reads this summary instead of the raw history, will it inherit the durable project meaning without inheriting unnecessary detail?

If the answer is no, the summary is either too thin or too noisy.

---

## 3. Standard Summary Structure

All summaries should share a common base structure so they remain predictable and skimmable.

Recommended base structure:

```md
# Summary

## Scope

## Period

## Key Outcomes

## Durable Decisions

## State Changes

## Unresolved Items

## References
```

Optional sections:

- `## Supersedes`
- `## Superseded By`
- `## Notes on What Was Discarded`

## 3.1 Section meanings

### `## Scope`
What this summary covers.

### `## Period`
Which sessions, days, week, or milestone range it compresses.

### `## Key Outcomes`
What materially changed.

### `## Durable Decisions`
Which decisions must still be remembered.

### `## State Changes`
How project understanding or active state evolved.

### `## Unresolved Items`
What remains open and should still be tracked.

### `## References`
Pointers to canonical files, lower-level summaries, or archive ranges when detail is needed.

## 3.2 Format guidance

Summaries should:

- prefer bullets to long prose
- be understandable in one read
- stand alone well enough to reduce archive-reading cost
- remain compact enough for version control and context loading

---

## 4. Daily Summary

## 4.1 Purpose

A Daily Summary is the first compression layer above raw sessions.

It should compress one day of work into a coherent historical artifact.

## 4.2 What a Daily Summary should preserve

- the day’s meaningful changes
- decisions made that day
- work completed or materially advanced
- blockers that survived the day
- work that rolled into the next day

## 4.3 What a Daily Summary should discard

- repeated intra-day exploration
- every attempted approach
- minor debugging loops that did not change understanding
- chronology finer than needed to understand the day’s outcome

## 4.4 Recommended structure

```md
# Daily Summary

## Day Scope

## Completed Changes

## Important Decisions

## Remaining Work

## Active Risks / Open Questions

## Related Sessions
```

## 4.5 Design guidance

Daily summaries should be the most detailed summary tier.
They remain close enough to raw history to support tactical reconstruction, but should still be significantly cheaper to read than multiple session archives.

---

## 5. Weekly Summary

## 5.1 Purpose

A Weekly Summary is a second-order rollup.

It should compress multiple daily summaries into a more strategic view of the week.

## 5.2 What a Weekly Summary should preserve

- major progress areas
- decisions that materially affected direction
- unresolved risks that survived across multiple days
- workstreams still in motion at the end of the week
- the shape of the week’s progress

## 5.3 What a Weekly Summary should discard

- isolated daily details that no longer matter
- repeated daily status updates
- granular chronology when trend-level understanding is enough

## 5.4 Recommended structure

```md
# Weekly Summary

## Week Scope

## Major Progress

## Durable Decisions

## Cross-Cutting Risks

## Continuing Workstreams

## Carry-Forward into Next Week

## Related Daily Summaries
```

## 5.5 Design guidance

A weekly summary should not read like seven daily summaries pasted together.
It should preserve only the durable shape of the week.

---

## 6. Project Summary

## 6.1 Purpose

A Project Summary is a long-horizon rollup.

It should support:

- milestone transitions
- large context resets
- onboarding after long gaps
- high-level restoration of project continuity

## 6.2 What a Project Summary should preserve

- milestone outcomes
- architecture trajectory
- major decisions and reversals
- long-lived unresolved fronts
- the current strategic shape of the project

## 6.3 What a Project Summary should discard

- most tactical session-level detail
- day-by-day chronology
- details whose only value was temporary execution guidance
- lower-level context already safely carried by daily or weekly summaries

## 6.4 Recommended structure

```md
# Project Summary

## Milestone Scope

## Project Trajectory

## Major Decisions

## Structural Changes

## Open Fronts

## What Can Be Ignored Now

## Related Weekly Summaries
```

## 6.5 Design guidance

A project summary is not just a bigger weekly summary.
It should preserve the long arc of continuity while making it easier to forget historical detail that no longer deserves routine attention.

---

## 7. Summary Hierarchy

Chronora’s summary hierarchy should be explicit:

```text
sessions/
  -> daily summaries
    -> weekly summaries
      -> project summaries
```

## 7.1 Hierarchy rule

Higher-level summaries should normally be derived from lower-level summaries where possible.
They should not always require rereading every raw session archive.

## 7.2 Compression rule by level

Each higher level should:

- preserve less tactical detail
- preserve more durable meaning
- be faster to read
- be safer to load into limited context windows

---

## 8. Summary Lifecycle

Summaries are derived artifacts with their own lifecycle.

## 8.1 Create

A summary is created when lower-level history becomes expensive enough to justify compression.

## 8.2 Revise

A summary may be revised if it is inaccurate, unclear, or missing durable information.

## 8.3 Supersede

A summary may be superseded by a higher-level or better-compressed summary.

Examples:

- several daily summaries superseded by one weekly summary
- several weekly summaries superseded by one project summary

## 8.4 Retain

A summary should be retained when it still reduces reading cost or preserves useful context not carried elsewhere.

## 8.5 Deprecate

A summary can become non-primary for routine reading when a higher-level rollup replaces it.
This does not require deleting it.

## 8.6 Restore / Use

A summary may be used to restore project understanding or repair live-state drift before consulting raw archives.

## 8.7 Lifecycle rule

- canonical state is mutable truth
- summaries are derived compression
- archives are append-only evidence

The Summary Layer must never collapse these roles together.

---

## 9. Summary Retention Strategy

Retention should be based on reading value, not on historical completeness alone.

## 9.1 Daily summaries

Daily summaries may be superseded by weekly summaries once the relevant week is stable and well-compressed.
They may still be kept when tactical detail remains useful.

## 9.2 Weekly summaries

Weekly summaries should remain available until a project-level summary clearly subsumes them.

## 9.3 Project summaries

Project summaries should be retained the longest because they carry milestone-level continuity and offer the cheapest long-horizon reconstruction path.

## 9.4 Session archives

Raw session archives remain available even when summaries supersede lower-level summaries.
The archive remains the evidence layer.

## 9.5 Reading strategy

A future session should prefer:

1. the highest useful summary level first
2. lower summary levels only if needed
3. raw session archives only when ambiguity or verification requires them

---

## 10. Summary and `current.md`

`current.md` and summaries serve different roles.

## 10.1 Boundary

- `current.md` = what is true now
- summaries = compressed history explaining what still matters from the path that led here

## 10.2 Relationship rules

1. Summaries may inform `current.md`.
2. Summaries must not replace `current.md`.
3. Once a fact is fully absorbed into live truth, `current.md` becomes the primary operating surface for that fact.
4. Older contextual explanation can remain in summaries so `current.md` stays compact.
5. If `current.md` and a summary disagree, `current.md` wins as live truth until corrected explicitly.

## 10.3 Why this matters

Without this boundary, summaries become a second competing state system.
Chronora should avoid that failure mode.

---

## 11. Summary and `handoff.md`

`handoff.md` and summaries also serve different roles.

## 11.1 Boundary

- `handoff.md` = immediate baton-pass for the next session
- summaries = non-immediate compressed historical context

## 11.2 Relationship rules

1. `handoff.md` may point to one or more relevant summaries.
2. Summaries should reduce how much historical explanation must be duplicated in `handoff.md`.
3. `handoff.md` should stay short and action-oriented.
4. Summaries should carry background that matters, but not immediate next-step instructions.

## 11.3 Why this matters

A healthy handoff should not need to re-explain months of project history.
The Summary Layer exists partly to prevent that.

---

## 12. Restore Workflow

When continuity needs to be reconstructed after a long gap, archive growth, or state drift, Chronora should restore understanding in layers.

## 12.1 Recommended restore order

1. Read `current.md` for live truth.
2. Read `handoff.md` for immediate operating context.
3. Read the highest relevant summary level:
   - project summary first when available
   - weekly summary next when more detail is needed
   - daily summary when tactical clarification is required
4. Consult raw session archives only if ambiguity remains or evidence is required.
5. If live truth is wrong, explicitly repair canonical files.

## 12.2 Restore rule

Restore should flow:

- from compressed history
- into corrected live state

It should not turn history itself into the operating state.

---

## 13. Token Compression Strategy

The Summary Layer should reduce context cost through deterministic compression.

## 13.1 Compression principle

Compress by **durability**, not just by time.

What matters is not merely that something happened earlier.
What matters is whether it still affects future work.

## 13.2 Compression ladder

Chronora should support a layered reading model:

- raw archives = maximum detail, maximum token cost
- daily summaries = tactical compression
- weekly summaries = strategic compression
- project summaries = milestone compression
- `current.md` + `handoff.md` = immediate working set

## 13.3 What to preserve for token efficiency

To maximize useful compression, summaries should preserve:

- active constraints
- durable decisions
- unresolved blockers
- architecture shifts
- rationale that prevents repeated debate
- major progress milestones

## 13.4 What to discard for token efficiency

To maximize useful compression, summaries should discard:

- repeated exploratory reasoning
- alternative paths not chosen and no longer relevant
- verbose chronological replay
- transient logs and temporary debugging detail
- background already captured elsewhere in canonical state

## 13.5 Practical goal

The practical goal is:

> most future sessions should be able to load `current.md`, `handoff.md`, and the highest useful summary layer without rereading large transcript or archive volumes.

---

## 14. Preserve vs Discard Matrix

| Preserve | Why |
| --- | --- |
| durable decisions | prevents re-litigating important choices |
| architecture changes | changes how the project must be understood |
| unresolved blockers | still affects future work |
| corrections to prior assumptions | prevents carrying false truth forward |
| milestone progress | changes project state at a strategic level |
| deferred-but-important issues | may need later resumption |
| high-value rationale | explains why a lasting decision exists |

| Discard | Why |
| --- | --- |
| transcript filler | no continuity value |
| repeated alternatives not chosen | redundant after decision is settled |
| dead-end debugging without durable lesson | does not affect future work |
| temporary hypotheses disproven later | obsolete |
| exhaustive chronology | expensive but low-value once outcome is known |
| transient runtime noise | not project truth |
| detail already absorbed into canonical state | duplication reduces clarity |

---

## 15. Recommended Decisions

The recommended Summary Layer design is:

1. Summaries are a **derived compression layer**, never canonical truth.
2. The summary hierarchy should be:
   - daily
   - weekly
   - project
3. Higher summary levels should preserve less tactical detail and more durable meaning.
4. Restore should begin from `current.md` and `handoff.md`, then descend into summaries only as needed.
5. Raw session archives should remain the evidence layer.
6. Token compression should optimize for what still affects future work, not for preserving every step of reasoning.
7. Summary quality should be judged by durable information density, not by narrative completeness.

---

## Final Recommendation

Chronora should treat summaries as the memory compression layer between raw historical evidence and live project state.

That layer should:

- preserve durable meaning
- discard transient execution detail
- reduce reading cost
- reduce token cost
- support restore after long gaps
- keep canonical state compact and current

A good Summary Layer helps the project remember what matters without forcing the future to carry the full weight of the past.