# Functional Requirements

Requirements are grouped under **features** — a coarser, product-facing grouping of
related requirements. The blockquote under each heading is this repo's read on that
feature's intent/scope, not a spec in itself; the FR rows are the spec.

This app is a **relying party**: end users authenticate directly to it, either with a
password or by federating to Google, Microsoft, or GitHub. It does not issue OAuth tokens
to other applications — there is no client/application registration concept here.

## Account Registration & Authentication

> How a person gets an account and proves who they are: a password, or a federated
> identity from Google, Microsoft, or GitHub. Account linking (one person, two login
> methods converging on one account) lives here too, scoped to linking-by-verified-email
> only — no other linking heuristic (e.g. name matching) is in scope.

| ID | Requirement | Status |
|----|-------------|--------|
| FR-01 | A person can register an account with an email address and a password. | Documented — implementation pending |
| FR-02 | A person can log in with their email address and password. | Documented — implementation pending |
| FR-03 | A person can log in (registering on first use) via an OAuth/OIDC identity from Google, Microsoft, or GitHub. | Documented — implementation pending |
| FR-04 | When a social login's verified email matches an existing password-based account, the social identity is linked to that existing account instead of creating a duplicate. | Documented — implementation pending |
| FR-05 | A logged-in user can link an additional social identity (Google, Microsoft, or GitHub) to their account. | Planned |
| FR-06 | A logged-in user can unlink a social identity from their account, provided at least one other login method (password or another linked identity) remains. | Planned |

## Session Management

> What happens after a successful login: how a session is created, how long it lasts, and
> how a user ends it — on one device or all of them.

| ID | Requirement | Status |
|----|-------------|--------|
| FR-07 | A successful login (password or social) creates a session, identified to the browser by an HTTP-only session cookie. | Documented — implementation pending |
| FR-08 | A user can log out, immediately invalidating their current session. | Documented — implementation pending |
| FR-09 | A session that has been inactive beyond a configured idle timeout, or has reached its absolute lifetime, is no longer valid. | Planned |
| FR-10 | A user can view their active sessions (login method, device, last-seen time) and revoke any one of them remotely. | Planned |

---

FR-01, FR-02, FR-03 (with FR-04 as an extension), and FR-08 are detailed in
`docs/usecases/uc-01-register-with-password.md`, `uc-02-login-with-password.md`,
`uc-03-login-with-oauth-provider.md`, and `uc-04-logout.md`. FR-07 is satisfied as a shared
step inside UC-02 and UC-03 rather than its own use case. FR-05, FR-06, FR-09, and FR-10
are headings only until their use cases are written (see the `new-use-case` skill).
