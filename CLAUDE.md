# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

An OAuth/identity exploration for an enterprise-style web app: a FastAPI backend (DDD +
hexagonal architecture) and a Next.js frontend, backed by PostgreSQL + Redis, orchestrated
with Docker Compose. This app is a **relying party only** — end users authenticate
directly to it, either with an email/password or by federating to Google, Microsoft, or
GitHub via OAuth/OIDC, and the app manages their session afterward. It does not issue
OAuth tokens to other applications; there is no client/application registration concept.

The backend is a clean slate: only the composition root (`main.py`, a bare FastAPI app
with a `/health` check) and the generic `IdGenerator` port/`UuidGenerator` adapter exist.
No use case from `docs/usecases/` is implemented yet — start with UC-01 per the
doc-first workflow below. The frontend is still the unmodified `create-next-app` starter.

## Doc-first workflow (V-Model)

This repo works top-down through `docs/`, and code should never get ahead of what's
documented there:

1. **Requirement** — `docs/requirements/functional.md` (FR-NN) / `non-functional.md`
   (NFR-NN). Scaffold with the `new-requirement` skill.
2. **Use case** — `docs/usecases/uc-NN-*.md` + a `.puml` sequence diagram, for every FR
   that describes a user-facing capability. Scaffold with the `new-use-case` skill.
3. **Architectural decisions that don't fit one use case** (e.g. how sessions are stored,
   how OAuth providers are adapted) go in `docs/adr/` instead — see ADR-0001 and ADR-0002.
   Scaffold with the `new-adr` skill.
4. **Implementation** — TDD, inside-out: domain → application → driven adapter → driving
   adapter. Use the `tdd` skill.
5. **Traceability** — `docs/v-model/traceability.md` maps every requirement to its use
   case and real test file paths; a requirement isn't done until that row has no
   `planned` left in it.

`docs/engineering/README.md` walks through this loop in full (including the skill
catalog); `docs/architecture/glossary.md` and `docs/architecture/identity-domain-model.puml`
are the domain's vocabulary and tactical model (Entities/Value Objects/Aggregates);
`docs/architecture/context-map.puml` is the strategic view (this app's one bounded context,
Identity & Access, plus Google/Microsoft/GitHub as external systems). Commit conventions
live in `CONTRIBUTING.md`; branch naming in `docs/engineering/branching-strategy.md`.

## Hexagonal boundary rule (NFR-01)

`backend/src/app/domain/` and `backend/src/app/application/` must never import a
framework (FastAPI, an ORM, a Postgres/Redis client, an OAuth SDK). Only
`infrastructure/adapters/` is allowed to know about those. This is enforced by code
review today (no automated import-linter yet) — see `docs/requirements/non-functional.md`.

## Commands

### Backend (FastAPI, `/backend`)

```bash
cd backend
pip install -e .[dev]   # install package + dev deps (pytest, httpx)
pytest                  # run all tests
pytest tests/test_health.py                                    # run one file
pytest tests/test_health.py::test_health_check                 # run one test
```

There is no configured linter/formatter for the backend yet.

### Frontend (Next.js, `/frontend`)

```bash
cd frontend
npm install
npm run dev     # dev server at http://localhost:3000
npm run build
npm run lint     # eslint (flat config, next/core-web-vitals + next/typescript)
```

There is no test runner configured for the frontend yet.

### Full stack (Docker Compose)

```bash
docker compose up --build
```

Brings up frontend (`:3000`), backend (`:8000`, OpenAPI docs at `/docs`), Postgres (`:5432`), and Redis (`:6379`). The backend container reads `DATABASE_URL` and `REDIS_URL` from compose env vars, but nothing currently uses them — no persistence adapter exists yet. Per ADR-0001, Postgres is intended for `User` data and Redis for `Session` data once implemented.

## Backend architecture

Hexagonal / ports-and-adapters, organized under `backend/src/app/`:

- `domain/` — pure business objects and repository interfaces (ports), no framework dependencies. Empty today; the documented domain (`User`, `Session`, and their value objects) is specified in `docs/architecture/identity-domain-model.puml` and implemented one TDD increment at a time, per use case.
- `application/` — use cases and the ports they depend on.
  - `use_cases/` — empty today. One class per use case, taking a `Command` dataclass as input and depending only on domain interfaces, never concrete adapters. The documented use cases are `RegisterWithPassword`, `LoginWithPassword`, `LoginWithOAuthProvider`, `LogOut` (`docs/usecases/uc-01`..`uc-04`).
  - `ports/` — `IdGenerator` already exists (generic, reusable for `UserId`/`SessionId`). The documented domain also needs `UserRepository`, `SessionRepository`, `PasswordHasher`, `OAuthIdentityProvider`, `Clock` — none exist yet.
- `infrastructure/adapters/` — concrete implementations, swappable behind the domain/application interfaces.
  - `http/` — empty today. Will hold the FastAPI router(s) wiring use cases to `/auth/*` routes and their Pydantic schemas. This is the only driving adapter in this project — there is no MCP or other adapter.
  - `persistence/` — `UuidGenerator` (implements `IdGenerator`) already exists. The documented domain calls for `PostgresUserRepository`, `RedisSessionRepository`, and one `OAuthIdentityProvider` adapter per provider (`GoogleOAuthAdapter`, `MicrosoftOAuthAdapter`, `GithubOAuthAdapter`), per ADR-0002 — none exist yet.
- `main.py` — composition root: `create_app()` builds the FastAPI app. Currently wires nothing but a `/health` check; as use cases are implemented, this is where their adapters get instantiated and their routers mounted. `create_app()` is the factory used by both tests and the ASGI entrypoint (`app = create_app()`).

`backend/tests/test_health.py` is the only test today, confirming the composition root
boots. New tests follow the `tdd` skill's layout (e.g. `backend/tests/domain/`,
`backend/tests/application/`) as each use case is implemented.

## Frontend architecture

Standard Next.js App Router layout under `frontend/src/`:

- `app/` — routes, layouts, global styles (`globals.css`).
- `components/ui/` — shadcn/ui components (configured via `components.json`: style `default`, base color `neutral`, no Tailwind prefix, RSC-enabled). Add new shadcn components through the shadcn CLI rather than hand-rolling, to stay consistent with this config.
- `lib/` — shared utilities (e.g. `cn()` helper in `utils.ts`).

Path alias `@/*` maps to `frontend/src/*` (see `tsconfig.json`). The frontend has no `core/domain`/`core/application` layer yet; NFR-01's boundary rule applies to it once one exists.
