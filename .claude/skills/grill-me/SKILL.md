---
name: grill-me
description: Interview the user about implementation choices for a use case (or other design decision) before code gets written — one question at a time via AskUserQuestion, exploring the docs/code independently first, resolving every branch of the decision tree. Use before starting TDD on a use case in this repo, especially the first slice of a new layer or adapter, or whenever a plan needs pressure-testing before implementation.
---

# grill-me

Adapted from the community `grill-me` pattern (interview relentlessly until reaching
shared understanding), wired to this repo's V-Model + hexagonal conventions so it never
re-asks something already settled in docs or code.

## Input

`args` is a use case id (e.g. `uc-01`) or a short topic. If omitted, ask once which use
case or decision is being grilled, then proceed without further plain-text questions.

## Before asking anything

Read for yourself — never ask about something already answered by:

- the named use case's `.md` + `.puml` in `docs/usecases/`
- its related FR/NFR rows in `docs/requirements/`
- every ADR in `docs/adr/` (architecture-level decisions live there, not here)
- `CLAUDE.md` (hexagonal boundary rule, doc-first ordering, layering order)
- any existing code under `backend/` or `frontend/`, for prior art / established
  conventions to stay consistent with

Only bring the user questions that are genuinely open: not answered by the docs, not
implied by an existing pattern in the code, not dictated by `CLAUDE.md` or an ADR.

## Process

1. Build the decision tree for the slice about to be implemented, grouped into branches
   (see "Question categories" below for the usual set on this repo's backend).
2. Ask one question at a time using `AskUserQuestion`, with 2–4 realistic options informed
   by what was found in the codebase/docs — never a bare open-ended question when the
   options are enumerable. Never ask in plain text; always use the tool.
3. Acknowledge the answer in 1–2 sentences, then immediately ask the next question whose
   prerequisites are now settled. Don't queue multiple questions in one turn.
4. If an answer opens a new branch (e.g. choosing Postgres over an in-memory fake raises a
   schema/migration question), add it to the tree and keep going.
5. Stop asking once every branch for *this* slice is resolved. Don't ask about things that
   don't matter yet (e.g. don't grill update/delete semantics while grilling create-note).
6. Close with a compact written summary of every decision made, organized by layer
   (domain → application → driven adapter → driving adapters).
7. Flag which decisions are big enough to warrant an ADR (per `CLAUDE.md`: "architectural
   decisions that don't fit a use case") vs which just become code, and ask whether to:
   scaffold an ADR (`new-adr` skill) first, proceed straight to TDD implementation, or
   stop here.

## Question categories to consider (skip any already settled)

- **Domain modeling** — value objects vs primitives for `Email`/`PasswordCredential`/
  `OAuthProvider`/`SessionId`; where validation rules live (password policy, email format);
  what a validation failure looks like as a type. For every concept being modeled, classify
  it as an Entity (has identity via an id; equality must be identity-based, e.g. two
  `User`s with the same `UserId` are the same user even if their email/credential differs)
  or a Value Object (equality is by value; interchangeable if equal) per Evans/Vernon's DDD
  tactical patterns — don't leave this implicit. If it's an Entity, explicitly ask whether
  the language's default equality needs overriding (e.g. a Python frozen dataclass's
  auto-generated `__eq__` compares *all* fields, which is Value Object semantics, not
  Entity semantics — it will need a manual `__eq__`/`__hash__` by id instead). Also confirm
  which aggregate root this concept belongs to — `User` or `Session` (see
  `docs/architecture/glossary.md`) — since that's what the repository operates on.
- **Ports** — exact shape of `UserRepository`/`SessionRepository`, `PasswordHasher`,
  `OAuthIdentityProvider`, `IdGenerator`, `Clock`; sync vs async; what `save()` returns;
  whether ports live under `domain/` or `application/`.
- **Persistence for this increment** — in-memory fake first (keeps TDD inside-out, defers
  the Postgres/Redis adapter) vs implementing `PostgresUserRepository`/
  `RedisSessionRepository` immediately; if Postgres, schema/migration approach now vs
  later.
- **Error handling** — exception hierarchy; where domain errors get translated to
  application errors; exact HTTP status at the boundary (e.g. UC-02's deliberately
  indistinguishable 401 for "no such user" vs "wrong password," to avoid user
  enumeration).
- **Testing** — what's a unit test vs a contract test vs the acceptance test for this UC;
  what row this adds to `docs/v-model/traceability.md`.
- **Project scaffolding** — the backend is a clean slate besides the composition root and
  `IdGenerator`/`UuidGenerator` (see `CLAUDE.md`), so this applies to the first use case's
  first increment: package manager/tooling, test runner, directory layout under `backend/`,
  how the composition root (`main.py`) wires ports to adapters.
- **OAuth provider adapter wiring** — for UC-03 specifically: build and prove the
  `OAuthIdentityProvider` port against one provider (e.g. Google) first, or stub all three
  immediately since ADR-0002 already fixes the port shape.

## Non-goals

- Doesn't write code or docs itself — hands off to `new-adr`, TDD, or direct
  implementation once decisions are made.
- Doesn't ask about anything a skim of the docs/code already answers — that burns the
  user's attention on settled questions, which defeats the point of grilling one thing at
  a time.
