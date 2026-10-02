---
name: tdd
description: Implement a use case (or a scoped increment of one) via strict Red-Green-Refactor, one small step at a time, pausing to show the test and then the implementation before either is committed. Use when the user wants to start or continue TDD on a use case in this repo, says "write the test first"/"red-green", or invokes /tdd.
---

# tdd

Adapted from the community `tdd` skill pattern (strict Red-Green-Refactor with a pause
after RED to review the failing test), wired to this repo's V-Model/hexagonal conventions:
increments come from the use case doc itself, not a freeform feature description, every
GREEN step is checked against the hexagonal boundary rule before it's allowed to land, and
nothing is committed without being shown and approved first — a passing test suite is
evidence the code works, not evidence it has been reviewed.

## Input

`args` is a UC id (`uc-01`) and optionally a starting layer/increment (e.g. "uc-01 domain"
to resume partway through). If omitted, infer the UC id from the current branch name
(`feat/UC-NN-...`, per the `new-branch` skill's convention) rather than asking. If neither
gives an id and this isn't pure tooling/scaffolding work, ask once which use case this is
for — don't start writing tests for undocumented behavior (see `CLAUDE.md`'s doc-first
rule).

## Phase 0: Plan the increments

1. Read the named use case's `.md` + `.puml`. Each numbered `[UC-NN.n]` step and each
   lettered extension (e.g. `3a`) is a candidate increment. Order them per `CLAUDE.md`'s
   layering rule: domain → application → driven adapter → driving adapter (REST — there is
   no MCP or other driving adapter in this project, see `CLAUDE.md`).
2. Confirm the language/test runner from what already exists (`backend/pyproject.toml` →
   plain `pytest`, run after `pip install -e .[dev]`; `frontend/package.json` → its test
   script, none configured yet) rather than asking, unless neither exists yet, in which
   case this is also the first backend/frontend code — say so and confirm the
   layout/tooling decided earlier (grill-me/ADR) before scaffolding it.
3. Present the increment list with `AskUserQuestion` (accept as-is / reorder / add / drop)
   before starting — one confirmation up front, not one per increment.
4. Track progress as a plain numbered list in your responses (increment N of M); update it
   after each increment completes rather than re-listing from scratch.

## Phase 1: RED — one increment at a time

1. Write the failing test directly into the real test file (mirror existing layout, e.g.
   `backend/tests/domain/test_user.py`), named for the behavior it verifies. One
   assertion/behavior per test; start from the simplest/degenerate case for this increment
   before the general case. Give it a docstring with three parts: the use case step it
   covers and the criterion in plain words (`UC-01.3a: Title must be non-empty.`), one
   sentence on why it matters, and a `Requirement: FR-xx.` line — or `Requirement: none
   (...)` with a short reason, for a test that follows from a language or DDD-modeling
   invariant rather than a stated requirement (e.g. a hash/equality contract). Reuse the
   use case's own step numbering as the identifier; don't invent a second, parallel
   numbering scheme for the same thing.
2. Run just that test. Confirm it fails **for the expected reason** (assertion failure on
   the behavior under test) — not an import error, typo, or a pass-by-accident. If it
   passes unexpectedly or fails for the wrong reason, stop and say so before continuing;
   don't paper over it. Do not commit yet — the test and the implementation that turns it
   green land together in one commit, made at the end of Phase 2.
3. Show the test's full content in the response (not just the failure output), then pause
   with `AskUserQuestion` ("test fails as expected — ready for GREEN?" / "change the test
   first"). Reviewing the failure alone is not reviewing the test; the point of this
   checkpoint is for the test itself to be read before any implementation exists to react
   to it — don't design or think ahead about the implementation while writing the test.

## Phase 2: GREEN — minimal code, no more

1. Write the smallest implementation that makes the new test pass. Nothing extra —
   no handling for cases no test asks for yet. When this increment corresponds to a named
   message in the use case's `.puml` (a method name or a DTO name — e.g.
   `Port -> Postgres : [UC-01.6] save(user)` naming the method `save`), the implementation
   must use that exact name. The diagram was written before the code specifically so its
   names are load-bearing, not illustrative; if a name genuinely needs to change once
   writing the code makes something clearer, amend the `.puml` in the same commit as a
   visible decision — never let the code quietly drift from a name the diagram still shows.
2. If this increment touches `domain/`, `application/`, `core/domain/`, or
   `core/application/`: check the diff imports nothing from a framework (FastAPI,
   psycopg/asyncpg, redis, an OAuth provider SDK, Next.js, fetch) per `CLAUDE.md`'s
   hexagonal boundary rule. If it does, stop —
   that logic belongs in an adapter behind a port, not here.
3. Run the **full** test suite, not just the new test.
4. If everything passes: show the implementation's full content in the response (not just
   "tests pass"), then pause with `AskUserQuestion` ("commit this?" / "change it first").
   Nothing is committed until this is answered — a passing test suite is not the same
   thing as the change having been seen. Do not run `git commit` as part of answering the
   question in the same turn as showing the diff; wait for the next turn's answer.
5. Once approved: commit the test and the implementation together, one commit,
   `feat(<scope>): <summary>` (or `fix(<scope>):` if it's correcting a prior increment) —
   the type describes the behavior added, since the commit is the whole increment, not
   just its test.
6. If something else broke at step 3: show the failure and pause — ask whether to fix it
   now or hand it back. Never commit with a red suite (`CONTRIBUTING.md`).

## Phase 3: REFACTOR

1. Look for duplication, naming, or extraction opportunities introduced by this increment.
   If any exist, apply them and re-run the full suite to confirm still-green; fold the
   change into the increment's commit if trivial, or a separate `refactor(<scope>):` commit
   if substantial enough to want its own message.
2. If nothing needs refactoring, say so and move on — no forced busywork.
3. If a refactor breaks a test, revert it and pause rather than debugging under pressure to
   keep moving.

## Phase 4: traceability and domain docs, then next increment

1. When an increment is the *first* test of a given test type for this UC (first domain/
   application unit test, first adapter contract/integration test, first end-to-end
   acceptance test through REST), update the matching cell in the `FR-xx | UC-NN`
   row of `docs/v-model/traceability.md` — replace `planned` with the real test file path.
2. When an increment changes the domain's shape (a new Entity or Value Object, a change to
   which class is the aggregate root, a new domain event, or a change to what makes two
   instances equal), update `docs/architecture/<context>-domain-model.puml` and, if the
   change affects a term's definition or classification, `docs/architecture/glossary.md`.
   These two files describe the domain as it has actually been built; they are updated
   after the increment is green, not before, and only when the increment actually changes
   what they describe.
3. Return to Phase 1 for the next increment. No pause between increments beyond the two
   checkpoints already in the loop: the RED review in step 1.3 and the pre-commit review
   in step 2.4.

## Wrap-up

Once every planned increment for this pass is done: summarize what was added (increment →
test → commit), confirm which `traceability.md` cells were updated, and name what's left
(e.g. the Microsoft/GitHub provider adapters if only Google was in scope for UC-03, or
link/unlink if only login was in scope) — don't silently expand scope to cover it now.

## Rules

- Never write implementation before a test exists and has been confirmed red for the right
  reason.
- Never run `git commit` in the same turn as writing the code it would commit. Show the
  test (end of Phase 1) or the implementation (end of Phase 2) in full, ask, and commit
  only after an explicit approval arrives in a later turn. A green test suite is not
  approval.
- Never invent an increment the use case doc doesn't call for — a good idea that's out of
  scope (e.g. update/delete while implementing create) gets noted, not implemented.
- Test and implementation land together in one commit per increment (per
  `CONTRIBUTING.md`, splitting them is permitted, not required, and only worth doing when a
  commit is deliberately meant to teach the red/green cycle on its own). A test that passes
  immediately with no implementation change (a characterization test) is still its own
  commit, since there is no implementation to pair it with. Refactor may ride along in the
  same commit if trivial, or get its own follow-up commit if substantial — never left
  uncommitted with a red suite.
- Match conventions already established for this codebase/UC (layout, value-object style,
  error hierarchy) instead of re-deciding them per increment — if genuinely undecided,
  that's a `grill-me` gap, not a `tdd` one.
- When an increment introduces a concept with an id (an Entity or aggregate root, per a
  prior `grill-me`/domain-model doc), its own increment must drive out identity-based
  equality explicitly (e.g. a test asserting two instances with the same id but different
  other fields are equal, and two with different ids but identical other fields are not) —
  never assume the language's default equality (e.g. a Python dataclass's auto-generated
  `__eq__`, which compares all fields) is correct for it without a test proving so.
