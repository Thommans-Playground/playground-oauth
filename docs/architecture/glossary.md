# Glossary

The ubiquitous language (Evans) and tactical DDD model for each bounded context in
`context-map.puml`. Ubiquitous language is scoped *per context* — a term's meaning here
isn't assumed to hold in a future context; this file grows a new section (or splits into
one file per context) if a second context is ever built.

This is the domain's *vocabulary and tactical building blocks* (Entity, Value Object,
Aggregate). It is not the hexagonal architecture (how code is layered into
domain/application/infrastructure) — that's `CLAUDE.md`'s boundary rule and ADR-0001/0002.

## Identity & Access context

See `identity-domain-model.puml` for this context's two aggregate boundaries and
composition relationships as a class diagram — this table is the *why*, that diagram is
the *shape*.

| Term | Kind | Definition |
|---|---|---|
| User | Entity, **Aggregate Root** | A registered person. Has identity (`UserId`) that persists across password changes, email changes, and identity linking/unlinking — equality is by id, not by content. |
| UserId | Value Object | A user's identity. Two `UserId`s are the same user reference iff their values are equal. |
| Email | Value Object | A user's email address: validated format, compared case-insensitively. Used both as a login handle (UC-02) and as the account-linking key for social logins (FR-04, UC-03). |
| PasswordCredential | Value Object | A salted password hash plus the hashing algorithm identifier, produced by the `PasswordHasher` port (NFR-02). Optional on a `User` — an account created via social login only (UC-03) has none until FR-05 adds a password. |
| LinkedIdentity | Entity | One federated identity linked to a `User`: `OAuthProvider` + the provider's own user id + when it was linked. Has identity (the pair of provider + provider user id) distinct from the `User` it belongs to, but is only ever reached through its owning `User` — never persisted or looked up independently. |
| OAuthProvider | Value Object | One of `GOOGLE`, `MICROSOFT`, `GITHUB` — the fixed, closed set of providers this app federates to (ADR-0002). |
| Session | Entity, **Aggregate Root** | A single authenticated browser session: `SessionId`, the `UserId` it belongs to, `auth_method` used to create it, `created_at`, `expires_at`. A separate aggregate from `User` — different lifecycle (ephemeral, Redis-backed per ADR-0001) and different repository. |
| SessionId | Value Object | A session's identity: an opaque, high-entropy token. Two `SessionId`s are the same session reference iff their values are equal — never derived from or decodable into user data (ADR-0001). |

**Aggregate boundaries**:
- `User` is the aggregate root for `Email`, `PasswordCredential`, and every
  `LinkedIdentity` — none of these are persisted or looked up independently of the `User`
  they belong to, per Evans' aggregate rule. Account linking (FR-04) is a mutation of the
  `User` aggregate (adding a `LinkedIdentity`), not a separate operation on `LinkedIdentity`
  itself.
- `Session` is its own aggregate root, referencing a `User` only by `UserId` — not by
  embedding the `User` itself. A `Session` never reaches into `User`'s internals, and a
  `User` operation never needs to touch `Session`.

**Why this distinction matters in code**: an Entity's equality must be identity-based
(same id → same entity, even with different attribute values); a Value Object's equality
is by value. Getting this backwards is easy to miss in Python, where
`@dataclass(frozen=True)` auto-generates a *value*-based `__eq__` — `User`, `LinkedIdentity`,
and `Session` each need a deliberate identity-based `__eq__`/`__hash__` instead of the
dataclass default, for exactly this reason (see the `tdd` skill's identity-equality rule).

**Repositories**: `UserRepository` operates on `User` only; `SessionRepository` operates
on `Session` only — one repository per aggregate root, per Evans' rule, never per Value
Object or child entity (`LinkedIdentity` has no repository of its own).
