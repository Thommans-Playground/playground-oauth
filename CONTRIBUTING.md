# Contributing

This repo practices a doc-first V-Model loop (requirement → use case → TDD
implementation → traceability) over a DDD + hexagonal architecture. See `CLAUDE.md` for
the architecture rules and `docs/engineering/README.md` for how the loop fits together.

## Commit Messages

[Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <summary>`,
optionally followed by a body and a `Refs:` line.

**Types:** `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.

**Scopes** — the layer or area actually changed:

| Scope | Covers |
|---|---|
| `domain` | `backend/src/app/domain/` — entities, value objects, repository interfaces |
| `application` | `backend/src/app/application/` — use cases, ports |
| `http` | `backend/src/app/infrastructure/adapters/http/` — REST router, schemas |
| `persistence` | `backend/src/app/infrastructure/adapters/persistence/` — Postgres/Redis adapters |
| `oauth` | Provider-facing OAuth integration code (`OAuthIdentityProvider` adapters) |
| `frontend` | Anything under `frontend/` |
| `docs` | `docs/` changes only |

Tooling/scaffolding with no clear scope (`.claude/skills/`, root config) omits the scope
entirely: `chore: ...`. If a change spans multiple scopes and isn't one logical unit,
split it into separate commits rather than picking an arbitrary scope.

**Refs line:** `Refs: FR-NN[, UC-NN][, ADR-NNNN]` when the commit implements or documents
a requirement, use case, or architectural decision traced in
`docs/v-model/traceability.md`. Omit it for pure tooling/scaffolding commits.

**No attribution trailers.** Commit messages end at the `Refs:` line — no
`Co-Authored-By:` or "Generated with ..." trailer, regardless of what a tool would add by
default.

## TDD Granularity

Red-green-refactor, per the `tdd` skill: a test asserting new behavior lands together
with (or immediately before) the implementation that makes it pass, in one commit per
increment — splitting them is permitted, not required. Never commit with a red test
suite.

## Branching

Trunk-based development. See `docs/engineering/branching-strategy.md` for branch types
and naming.

## Pull Requests

A PR must be reviewed and pass all checks before merging to `main`.
