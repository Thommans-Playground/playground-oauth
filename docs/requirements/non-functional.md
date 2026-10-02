# Non-Functional Requirements

| ID | Requirement | Rationale |
|----|-------------|-----------|
| NFR-01 | `domain/` and `application/` (backend) must have zero framework imports. The frontend adopts the same rule for its own `core/domain`/`core/application` once it has one. | Hexagonal boundary — keeps business logic testable and framework-agnostic; the whole point of this repo's practice. |
| NFR-02 | A password is never stored or logged in plaintext — only a salted hash, produced and verified through the `PasswordHasher` port, is persisted or compared. | This is an identity system for an enterprise app; a plaintext or reversibly-encrypted password is the single most damaging credential leak possible. |
| NFR-03 | Every OAuth/OIDC authorization-code exchange with Google, Microsoft, or GitHub uses the `state` parameter to bind the callback to the request that started it, and PKCE where the provider supports it. | Prevents authorization-code interception and cross-site request forgery against the login flow — the baseline OAuth security practice this repo exists to exercise. |
| NFR-04 | The session cookie is `HttpOnly` and at minimum `SameSite=Lax`; it is also marked `Secure` in any non-local environment. | Session hijacking via script access (XSS) or cross-site submission is the main risk of a cookie-based session (ADR-0001). |
| NFR-05 | No requirement is considered done until it traces to at least one acceptance test in `docs/v-model/traceability.md`. | V-Model discipline — top and bottom of the V must connect. |
| NFR-06 | Local requests should complete well under a second against Postgres/Redis on a dev machine; no formal SLA. | This is a learning/exploration app, not a production service — keep NFRs proportionate. |
