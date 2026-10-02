# ADR 0002: One OAuthIdentityProvider Port, One Adapter per Provider

## Status

Accepted.

## Context

Three external OAuth/OIDC providers (Google, Microsoft, GitHub) must each support
"sign in with `{provider}`" (FR-03), with more potentially added later. Two patterns were
considered:

- **Pattern A:** A separate use case per provider (`LoginWithGoogle`, `LoginWithMicrosoft`,
  `LoginWithGithub`), each importing that provider's SDK or HTTP calls directly inside
  `application/`.
- **Pattern B:** One `LoginWithOAuthProvider` application use case, parameterized by
  provider, calling a single `OAuthIdentityProvider` port (`authorization_url()`,
  `exchange_code()`). A driven adapter per provider (`GoogleOAuthAdapter`,
  `MicrosoftOAuthAdapter`, `GithubOAuthAdapter`) implements that port, each translating its
  provider's own token/userinfo response shape into this app's normalized
  (`provider_user_id`, `verified_email`) pair.

## Decision

Use Pattern B.

## Rationale

The three providers differ only in their authorization/token/userinfo endpoint shapes and
scopes — the account-lookup, account-linking (FR-04), and session-creation logic
(UC-03 steps 5–7) is identical regardless of which provider authenticated the person.
Pattern A would duplicate that logic three times and let three different use cases each
reimplement the linking rule, which is exactly the kind of drift hexagonal architecture
(NFR-01) exists to prevent. Pattern B keeps `application/` provider-agnostic and makes
adding a fourth provider (e.g. Okta) a driven-adapter-only change — no new use case, no
domain change, no touching the account-linking rule.

## Consequences

- The composition root selects which `OAuthIdentityProvider` adapter to inject based on
  the `{provider}` path segment; adding a provider means registering one more adapter
  there, not branching application logic.
- Every provider adapter must normalize its userinfo response to the same
  (`provider_user_id`, `verified_email`) shape before returning. A provider that cannot
  guarantee a verified email (UC-03 extension 4b) cannot be supported without that
  constraint being revisited first.
