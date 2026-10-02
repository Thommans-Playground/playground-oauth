---
name: conformance-check
description: Check a requirement, use case, ADR, or domain/application code against the actual named industry practice for its type (Cockburn's use-case writing, Evans/Vernon's DDD tactical patterns, Nygard's ADR format, Beck's TDD, hexagonal architecture's port/adapter discipline) — not just this repo's own stated rules. Skips anything already covered by a `> **Exception:**` note. Use when asked to verify, audit, or check something against best practices/industry standards, or before closing out a use case, requirement, ADR, or implementation slice.
---

# conformance-check

Checks an artifact against the real methodology it claims to follow, using each
methodology's own named source as the rubric — not a restatement of `CLAUDE.md`. This is
about *pattern/method conformance*, not correctness or security: for bugs, use
`/code-review`; for vulnerabilities, `/security-review`. Run this alongside those, not
instead of them.

## Input

`args` is what to check: a file path, an artifact id (`FR-01`, `UC-01`, `ADR-0001`), "the
last commit", "everything since `<ref>`", or empty (defaults to whatever this
conversation just created or edited).

## Steps

1. Identify the artifact type(s) in scope from the target: requirement, use case, ADR,
   domain code, application code, adapter code, or commit. A target can span more than
   one (e.g. a use case plus its FR).
2. For each artifact, apply the rubric below for its type. Only check what's actually
   present — don't fault a doc-only repo for missing code-level checks.
3. Before flagging a gap, check whether the artifact already carries a
   `> **Exception:** ...` note (or equivalent stated reasoning) covering that specific
   point. If so, record it as **acknowledged**, not a defect — the point of the
   convention is that a deliberate, explained deviation isn't a finding.
4. Report three groups: **Gaps** (unaddressed, no exception — should be fixed or given an
   Exception note), **Acknowledged exceptions** (deviation exists and is explained),
   **Conformant** (nothing to flag). Don't editorialize beyond the rubric — if a check
   doesn't apply here (e.g. no aggregates exist yet), say so and move on.
5. Don't edit files. This skill reports; fixing or adding an Exception note is a separate,
   explicit follow-up.

## Rubrics

### Requirements (`docs/requirements/`)

- Testable and unambiguous — no "fast", "user-friendly", "robust" without a measurable
  threshold (NFR-04 is the model: states there's deliberately no formal SLA, with why).
- Atomic — one requirement per row, not two joined by "and"/"or".
- Independent — doesn't silently presuppose another undocumented requirement.
- (Loosely, the testable/unambiguous/independent slice of INVEST, applied to requirements
  rather than user stories.)

### Use cases (`docs/usecases/`)

Per Cockburn, *Writing Effective Use Cases*:

- Actor and goal are stated at the user-goal level, not the UI level ("log in with
  Google", not "click the Google button").
- Preconditions are actually checkable before the scenario starts, not narrative
  set-dressing.
- Main Success Scenario is the *unconditional* happy path — any branching belongs in
  Extensions, keyed to the step it branches from (this repo's `3a`/`4a` style).
- Each step advances the goal and names who does it (actor, driving adapter, application,
  domain, driven adapter) — matches this repo's layer-per-step convention.
- Postconditions state what's guaranteed true afterward, not a restatement of the last
  step.

### ADRs (`docs/adr/`)

Per Michael Nygard's ADR format:

- One architecturally significant decision per record — not a grab-bag of several.
- Context section states the forces/options neutrally, before the decision is revealed.
- Status is honest (`Proposed`/`Accepted`/`Superseded by ADR-000N`) — an accepted ADR is
  not edited to reflect a later reversal; a new ADR supersedes it instead.
- Consequences includes real tradeoffs, not just upside.

### DDD tactical patterns (`domain/`, once code exists)

Per Evans (*Domain-Driven Design*) and Vernon (*Implementing Domain-Driven Design*):

- Entities have identity and equality by id, not by attribute values.
- Value objects are immutable and compared by value.
- An aggregate enforces its own invariants; the aggregate root is the only mutation entry
  point (no reaching into an aggregate's internals from outside).
- No anemic domain model — behavior lives on the aggregate/value object, not scattered
  across services operating on public getters/setters.
- Repositories are defined only for aggregate roots, not for every entity.
- `docs/architecture/glossary.md` and `docs/architecture/<context>-domain-model.puml`
  still match the code: every Entity, Value Object, and Aggregate Root that exists in code
  is documented, with the same classification; nothing documented has since been removed
  or renamed in code without the document being updated to match.

### Hexagonal architecture (`domain/`, `application/`, `infrastructure/`)

Per Cockburn's ports & adapters:

- Ports (interfaces) are owned by the inside (domain/application) and implemented by
  adapters — dependency points inward, never outward (this is NFR-01, made explicit here
  against the pattern it's named after).
- Adapters translate at the boundary; no adapter-specific type (ORM row, HTTP request,
  an OAuth provider's raw token/userinfo response) crosses into domain/application.
- Composition root is the only place adapters are wired to ports — no adapter constructs
  another adapter directly.

### TDD (commit history, once code exists)

Per Kent Beck's red-green-refactor:

- A `test(...)` commit exists before the corresponding `feat(...)` commit for the same
  slice (this repo's own `CONTRIBUTING.md` granularity section already asks for this —
  verify it actually happened, don't just trust the intent).
- Tests assert observable behavior/outcome, not internal implementation details that
  would break on a valid refactor.

### Commits

Conventional Commits compliance is already the `commit` skill's job — `conformance-check`
only checks it if asked directly; don't duplicate that skill's work on every run.

## Output format

For each artifact: type, which rubric applied, and the three groups (Gaps / Acknowledged
exceptions / Conformant). Keep it terse — a bullet per point, not a paragraph. If nothing
in a category applies, omit that category rather than writing "None."
