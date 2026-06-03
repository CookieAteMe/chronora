# Chronora Architecture Review

## Review Scope

This document reviews the current Chronora architecture from a system-design perspective.

Reviewed documents:

- `docs/agent-adapter-architecture.md`
- `docs/chronora-core-state-contract.md`
- `docs/chronora-summary-layer-spec.md`
- `docs/chronora-restore-workflow-spec.md`

Supporting references:

- `README.md`
- `docs/philosophy.md`
- `docs/workflow.md`
- `docs/session-archive.md`

This is **not** an implementation review.
It is a review of responsibility boundaries, protocol consistency, dependency direction, MVP scope, and implementation feasibility.

---

## 1. Overall Assessment

Chronora's current architecture is **directionally strong and conceptually coherent**.

The strongest part of the design is its philosophical consistency:

- deterministic state over transcript replay
- explicit live truth over hidden memory
- append-only history over silent mutation
- continuity as a project-level protocol rather than a tool-specific behavior

The four documents largely reinforce the same worldview rather than competing with one another.
That is a strong sign.

However, the architecture also shows a familiar risk:

> the long-term conceptual system is clearer than the short-term core product boundary.

In other words, the architecture is promising, but the current surface is larger than what a v0.2 Core MVP should attempt to implement.

---

## 2. Architecture Strengths

### 2.1 Strong philosophical consistency

The entire document set consistently treats continuity as a **state problem** rather than a memory problem.

This is the right foundation for Chronora.
It makes the architecture portable, inspectable, and less dependent on any one coding agent.

### 2.2 Clear separation between live truth and history

The distinction among:

- canonical mutable state
- derived summaries
- append-only evidence

is one of the strongest parts of the architecture.

This separation reduces a common failure mode in AI workflows: confusing past reasoning with current truth.

### 2.3 Good long-term layering

The documents already imply a useful architectural stack:

- **canonical state** for current operations
- **summary layer** for durable compression
- **archive layer** for evidence
- **restore workflow** for continuity loading
- **adapter layer** for future runtime integration

This layering is clean and extensible.

### 2.4 Restore and summary models are compatible

The restore workflow and summary layer are not fighting each other.
They are broadly aligned:

- summaries reduce historical loading cost
- restore starts from live truth
- archives are consulted only when needed

That is an encouraging sign of system coherence.

---

## 3. Responsibility Overlap

## 3.1 `current.md` vs `handoff.md` vs `tasks.md`

This is the single biggest overlap risk in the current architecture.

### Current state of the design

- `current.md` owns live truth and includes `Next Steps`
- `handoff.md` owns immediate baton-pass and next-session actions
- `tasks.md` owns work inventory and active/blocked status

### Risk

All three documents can end up describing “what happens next.”
If not governed carefully, that creates duplication and drift.

Typical failure patterns would be:

- `current.md` says one next step
- `handoff.md` says a slightly different next action
- `tasks.md` shows a task state that implies something else

### Recommended boundary

Chronora should tighten the ownership model:

- `current.md` = durable situational truth
- `tasks.md` = operational work registry
- `handoff.md` = short-lived next-session baton only

### Review conclusion

This is **not yet a protocol conflict**, but it is a **high-probability operational overlap** unless the implementation and docs enforce stronger editorial rules.

---

## 3.2 Summary layer vs restore workflow

There is also moderate overlap between the summary-layer spec and the restore spec.

### Current state of the design

- the summary spec already defines how summaries support restore and token reduction
- the restore spec repeats the role of summary tiers and restore sequencing

### Risk

The same concepts are described from two directions, which can create future drift between documents.

### Recommended boundary

- `chronora-summary-layer-spec.md` should own **compression semantics**
- `chronora-restore-workflow-spec.md` should own **loading semantics**

### Review conclusion

This is **manageable overlap**, not a structural flaw.
But ownership should be made explicit as the docs evolve.

---

## 4. Protocol Conflicts

## 4.1 Maturity mismatch between architecture and current runtime

The most important tension is not logical inconsistency.
It is **maturity mismatch**.

### Current state

The architecture now assumes:

- `current.md`
- `tasks.md`
- `handoff.md`
- `summaries/`
- restore profiles
- future CLI restore/doctor concepts

But the actual shipped runtime still primarily supports:

- `.claude/current.md`
- `.claude/CLAUDE.local.md`
- `.claude/sessions/`
- `cclaude`

### Risk

Readers may confuse “architecturally defined” with “already implemented.”
That is especially likely because the docs are internally coherent.

### Review conclusion

There is **no severe protocol contradiction**, but there is a real risk of **implementation ambiguity** unless every future doc and README reference keeps separating:

- current shipped behavior
- v0.2 core target
- later architecture direction

---

## 4.2 Incomplete session metadata story

The adapter architecture references normalized session metadata, but there is no dedicated spec yet.

### Risk

Other documents sometimes assume richer session interpretation than the current archive format provides.

### Review conclusion

This is not yet a conflict, but it is a **missing contract boundary**.
For v0.2 Core MVP, this should probably stay intentionally narrow rather than being partially implied across multiple docs.

---

## 5. Circular Dependency Risks

Chronora does not currently have a fatal circular dependency problem.
But it does have **conceptual loop risk** if the roles are not enforced.

## 5.1 Potential loop surfaces

- restore uses summaries for efficient context
- summaries may be created from canonical state plus archives
- handoff may reference summaries
- canonical state may later be corrected after restore using summaries and archives

### Why this is acceptable today

The architecture remains acyclic if these rules hold:

1. canonical state is primary
2. summaries are derived
3. archives are evidence
4. restore consumes canonical state first, then summaries, then evidence

### Where the loop becomes dangerous

The system would become circular in practice if summaries were treated as alternate truth rather than derived compression.

### Review conclusion

There is **no hard circular dependency today**, but the architecture depends on one non-negotiable rule:

> summaries must never become canonical truth.

That rule should remain explicit everywhere.

---

## 6. Future Extension Risks

## 6.1 Namespace migration risk

The future move from `.claude/` to `.chronora/` is architecturally sensible, but operationally risky if done too early.

### Risk

- migration complexity
- compatibility burden
- split-state confusion
- documentation drift during transition

### Conclusion

This should remain a **post-core** concern.

---

## 6.2 Multi-agent ambition arriving before core state discipline

The adapter architecture is directionally strong, but it can easily pull the project into premature abstraction.

### Risk

If Chronora tries to solve cross-agent runtime integration before it proves the core continuity model operationally, it may optimize the wrong boundary first.

### Conclusion

Core state lifecycle should be proven before serious adapter work begins.

---

## 6.3 Manual maintenance burden

The current architecture introduces several durable artifacts:

- `current.md`
- `tasks.md`
- `handoff.md`
- summaries across multiple levels
- archives

### Risk

Even if conceptually clean, this can become operationally heavy if too much must be maintained by hand.

### Conclusion

The biggest long-term risk is not conceptual inconsistency.
It is **editorial overhead**.

---

## 7. Overdesign Risks

This is where the current architecture most needs tightening for v0.2 Core.

## 7.1 Multi-level summaries are likely too much for MVP

The daily / weekly / project hierarchy is useful as a long-term model.
But implementing that full hierarchy in the first core release would likely be premature.

### Risk

- too many artifact types before basic continuity discipline is proven
- too much manual summarization burden
- unclear payoff before archive volume actually grows

### Recommendation

For v0.2 Core, start with **one minimal summary model** or even make summaries optional.

---

## 7.2 Restore profiles may be too broad for first implementation

Fast / Normal / Deep restore is a good conceptual framework.
But as a product surface, this may be more than the core needs initially.

### Recommendation

For v0.2 Core, one default restore flow plus documented fallback behavior is enough.
Deep restore can remain a documented concept without full implementation commitment.

---

## 7.3 Cross-agent flows are architecture, not MVP

Claude → Codex → Gemini examples are valuable for showing that the protocol is agent-agnostic.
But they should not shape the core MVP surface.

### Recommendation

Keep cross-agent restore in architecture docs, but do not let it expand v0.2 implementation scope.

---

## 7.4 CLI vision may imply too much product surface

Commands like:

- `chronora restore`
- `chronora restore --deep`
- `chronora doctor`

are helpful future concepts.
But if treated as v0.2 requirements, they will broaden the build surface significantly.

### Recommendation

Treat them as **future interface concepts**, not core MVP commitments.

---

## 8. Implementation Difficulty Hotspots

## 8.1 Synchronizing canonical artifacts

The hardest practical problem is not file creation.
It is preventing drift among:

- `current.md`
- `tasks.md`
- `handoff.md`

This is a semantics problem, not a storage problem.

---

## 8.2 Summary creation and supersession

Even a good summary model becomes hard when the system must answer:

- when is a summary worth creating?
- when is it superseded?
- what level should be created first?
- what gets removed from routine reading?

This is likely too much policy surface for a first core release.

---

## 8.3 State-health checking

Detecting:

- stale handoff
- contradictory artifacts
- incomplete restore confidence
- damaged archive confidence

is useful, but nontrivial.

This belongs more naturally to a later health-check or doctor phase.

---

## 8.4 Namespace migration

Moving from `.claude/` to `.chronora/` is not technically hard in isolation.
But doing it without confusing users, examples, and continuity history is harder than it looks.

---

## 8.5 Review conclusion on difficulty

The hardest part of Chronora is not filesystem mechanics.
It is maintaining **clear state ownership with low duplication**.
That should guide MVP scoping.

---

## 9. Must Have / Should Have / Nice To Have

## 9.1 Must Have — v0.2 Core MVP

These are the smallest cohesive elements that make Chronora a real continuity layer rather than just a wrapper.

### Must Have

1. **Canonical live truth via `current.md`**
   - explicit, human-readable project state
   - clear update discipline

2. **Append-only session archive**
   - preserve before/after evidence
   - keep history separate from live truth

3. **One default restore rule**
   - load live truth first
   - use history only as fallback

4. **One lightweight handoff mechanism**
   - either a minimal `handoff.md` or a tightly scoped handoff section/pattern
   - enough to support next-session continuity without introducing a full planning surface

5. **Explicit live truth vs history distinction**
   - must remain visible in docs and runtime behavior

6. **Basic failure fallback guidance**
   - what to do when live state is wrong or missing

### Why this is the right MVP boundary

This set proves the core value proposition:

- explicit continuity state
- resumable workflow
- historical evidence
- deterministic restore

without yet requiring the full future system.

---

## 9.2 Should Have — v0.3 recommended

These are strong next-step features once the core loop is stable.

### Should Have

1. **`tasks.md` as operational work registry**
2. **minimal summary layer**
   - preferably one simple summary tier before full hierarchy
3. **clear stale-state detection guidance**
4. **restore confidence / fallback guidance beyond the basic flow**
5. **early doctor-style health-check design**

### Why they are not Must Have

They improve continuity quality, but they are not all required to prove the core thesis.

---

## 9.3 Nice To Have — future direction

These are valuable long-term directions, but should remain out of v0.2 Core scope.

### Nice To Have

1. full daily / weekly / project summary hierarchy
2. full fast / normal / deep restore modes as productized surfaces
3. `chronora doctor` and related health-check tooling
4. `.chronora/` namespace migration
5. normalized session metadata layer
6. adapter capability negotiation
7. cross-agent runtime integration
8. automated summary generation workflows

---

## 10. Chronora v0.2 Core MVP — Minimal Functional Set

The minimal functional set for **Chronora v0.2 Core MVP** should be:

1. **`current.md` as the canonical live truth**
2. **append-only session archives**
3. **a default restore protocol**
   - restore starts from `current.md`
   - archives are fallback evidence, not starting context
4. **a minimal handoff mechanism**
   - lightweight and tightly scoped
5. **clear documentation for correction and recovery when state drifts**

### Recommended exclusions from the MVP

The following should be intentionally deferred:

- full `tasks.md` operational model
- full multi-level summary hierarchy
- fast/normal/deep restore as productized features
- doctor tooling
- `.chronora/` migration
- adapter implementation or runtime abstraction

### MVP framing

A good v0.2 Core MVP is not “the whole continuity architecture.”
It is the smallest implementation that proves:

- explicit state beats transcript replay
- restore can start from project truth
- historical evidence can remain separate from live state
- continuity can survive across sessions without hidden memory

---

## 11. Recommended Next Step

Before expanding the surface further, Chronora should consolidate the core around:

- `current.md`
- archive continuity
- one restore flow
- one minimal handoff pattern

Only after that proves stable should it expand into:

- richer task state
- richer summary tiers
- doctor tooling
- deeper restore modes
- adapter-facing abstractions

---

## Final Conclusion

Chronora’s architecture is already **strong enough to guide the project**, but **too broad to implement all at once as v0.2 Core**.

The system does **not** currently suffer from major design contradictions.
Its main risks are:

- role overlap among state artifacts
- future documentation drift between compression and restore semantics
- operational maintenance burden
- MVP scope expanding faster than the core workflow is proven

The right move is not to redesign the architecture.
It is to **narrow the implementation target**.

Chronora v0.2 Core should focus on a minimal continuity backbone first, then grow into the fuller architecture that the current docs already describe.