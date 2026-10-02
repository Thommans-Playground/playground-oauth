---
name: new-requirement
description: Add a new functional (FR-NN) or non-functional (NFR-NN) requirement row to docs/requirements/, and stub its traceability row. Use as the first step of the doc-first V-Model workflow described in CLAUDE.md/AGENTS.md, before writing a use case with the new-use-case skill.
---

# new-requirement

Scaffolds the top of the V: a new requirement, before any use case or code exists for it.
Per `CLAUDE.md`, this is step 1 of the doc-first workflow — `new-use-case` comes after this,
not instead of it.

## Input

`args` is a short description of the capability or constraint, e.g. "user can unlink a
social identity" or "session lookups must not block on Redis for more than 200ms".

## Steps

1. Decide functional vs. non-functional from the description:
   - **Functional (FR):** a user-facing capability — usually phrased "A user can ...".
   - **Non-functional (NFR):** a quality attribute or constraint on the system itself
     (performance, architecture boundary, testability, security). If it's ambiguous, ask.
2. Find the next free id by reading `docs/requirements/functional.md` or
   `non-functional.md` (whichever applies) and incrementing the highest `NN` found.
3. Draft the requirement as one testable sentence:
   - FR row: `| FR-NN | <requirement> | Planned |` — match the imperative, testable style
     of existing rows (e.g. "A person can register an account with an email address and a
     password.").
   - NFR row: `| NFR-NN | <requirement> | <rationale> | ` — the rationale is the *why*,
     not a restatement of the requirement (see existing NFR-01..04 for tone). NFRs are
     cross-cutting and aren't grouped under a feature heading.
4. For an FR, decide which **feature** heading in `functional.md` it belongs under (e.g.
   "Account Registration & Authentication", "Session Management") by matching its intent
   against each heading's `>` blurb.
   If none fits, ask the user for a short feature name and a one-line `>` blurb on its
   intent/scope (not a restatement of the FR — see existing headings for tone), and add
   the new `## <Feature>` section with its own FR table.
5. Append the row to the correct table (under its feature heading for FR, or the flat NFR
   table), keeping ids in ascending order within each table.
6. Append a stub row to `docs/v-model/traceability.md`:
   - FR: `| FR-NN | (planned) | — | — | — |` (use case column stays `(planned)` until
     `new-use-case` fills it in).
   - NFR: `| NFR-NN | <use case ids if it's checked via a use case, else "—"> | planned or
     — per column, matching how NFR-01..04 are recorded> |`.
7. Do not write a use case or any code. Report the requirement id (and feature heading, for
   an FR) and remind the user: FRs need a use case next (`new-use-case`); NFRs may just
   need an enforcement mechanism (code review, lint rule, test) referenced from the
   traceability row instead.
