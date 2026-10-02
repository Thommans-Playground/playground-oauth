# ADR 0001: Server-Side Sessions in Redis, Not Stateless JWT

## Status

Accepted.

## Context

After a password or OAuth login (UC-02, UC-03), the app needs to recognize an
authenticated browser on every subsequent request. Two patterns were considered:

- **Pattern A — Stateless JWT:** Issue a signed JWT access token (plus a refresh token),
  carried by the client and verified on each request with no server-side lookup. Redis
  would only be used for a revocation/blacklist of tokens that must be invalidated early.
- **Pattern B — Server-side session:** Issue an opaque, high-entropy `SessionId` in an
  `HttpOnly` cookie. All session state (`UserId`, `auth_method`, `created_at`,
  `expires_at`) lives server-side in Redis; nothing is encoded in the cookie itself.

## Decision

Use Pattern B for this repo's session management (FR-07 through FR-10).

## Rationale

Immediate, reliable revocation — logout (FR-08), forced logout of a single device
(FR-10), and an eventual idle/absolute timeout (FR-09) — is a first-class requirement for
an enterprise identity system. With stateless JWTs, reliable revocation still needs a
server-side blacklist checked on every request, which erases the "no lookup" benefit JWTs
are chosen for while adding the complexity of two token types and signature verification.
An opaque session id also leaks nothing if intercepted — there's no signed payload to
decode — and Redis is already provisioned in `docker-compose.yml` for exactly this role.

The tradeoff accepted: every authenticated request costs one Redis lookup (acceptable
against NFR-06's non-production latency bar), and sessions do not scale across processes
without a shared Redis instance — already the plan here.

## Consequences

- `SessionRepository` is backed by Redis (a driven adapter), not Postgres — session data
  is ephemeral and expiring, unlike `User` data, which is durable.
- The session cookie carries only an opaque `SessionId` (NFR-04); no JWT parsing,
  signing, or verification logic exists anywhere in this stack.
- If true statelessness is later needed (e.g. a separate API consumed by native mobile
  clients without cookies), that is a new ADR, not a retrofit of JWT onto this design.
