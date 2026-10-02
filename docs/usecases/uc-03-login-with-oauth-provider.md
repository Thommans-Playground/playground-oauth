# UC-03: Log In with OAuth Provider (Google, Microsoft, or GitHub)

- **Primary Actor:** User (new or existing), via browser redirect
- **Trigger:** The actor chooses "Sign in with `{provider}`" and completes that provider's
  consent screen.
- **Preconditions:** None. This use case spans two separate HTTP requests (start and
  callback), unlike UC-01/UC-02's single request/response.

## Main Success Scenario

Each step is tagged `[UC-03.n]` on its corresponding message in
`uc-03-login-with-oauth-provider.puml`.

1. *Driving adapter* (REST `GET /auth/oauth/{provider}/start`) asks the
   `OAuthIdentityProvider` port for that provider's authorization URL, including a
   CSRF-binding `state` value and a PKCE challenge where the provider supports it
   (NFR-03), and redirects the actor's browser to it.
2. The actor authenticates with the provider and grants consent; the provider redirects
   the browser back to our callback URL with an authorization code and the original
   `state`.
3. *Driving adapter* (REST `GET /auth/oauth/{provider}/callback`) verifies the returned
   `state` matches the one issued in step 1, then calls *Application*
   (`LoginWithOAuthProvider` use case) with the authorization code.
4. *Application* calls the `OAuthIdentityProvider` port's `exchange_code()`. The *driven
   adapter* for that provider (e.g. `GoogleOAuthAdapter`) exchanges the code for tokens
   with the provider's token endpoint, then fetches the person's verified email and
   provider user id from the provider's userinfo endpoint, normalizing both into this
   app's own shape.
5. *Application* calls the `UserRepository` port to look up a `User` by
   (`provider`, `provider_user_id`) first, then — if not found — by the verified email.
6. *Domain*:
   - If no `User` matches either lookup, constructs a new `User` with a `LinkedIdentity`
     for this provider and no `PasswordCredential`.
   - If a `User` matches by email but has no `LinkedIdentity` for this provider, adds one
     to the existing aggregate (account linking, FR-04).
   - If a `LinkedIdentity` for this provider already exists, uses that `User` unchanged.
7. *Application* passes the `User` to the `UserRepository` port's `save()`, then
   constructs and saves a `Session` exactly as in UC-02 steps 5–7, with `auth_method` set
   to the provider's name.
8. *Driving adapter* sets the session cookie (as in UC-02 step 8) and redirects the actor
   back into the app, now logged in.

## Extensions / Exceptions

- **3a. `state` missing or does not match the one issued in step 1:** The callback is
  rejected before the application is called; mapped to HTTP 400. No session is created.
- **4a. The provider's token or userinfo exchange fails** (invalid/expired code, provider
  error): Application returns an authentication-failed error, mapped to HTTP 401 (or a
  login-failed redirect for the browser flow).
- **4b. The provider does not return a verified email:** Application rejects the login —
  there is no safe way to link or create an account without one — mapped to HTTP 401.

## Postconditions

- A `User` exists with a `LinkedIdentity` for this provider (new, or added to an existing
  account per FR-04).
- A `Session` exists for that `User`, with the same guarantees as UC-02's postconditions.

## Related Requirements

FR-03, FR-04, FR-07, NFR-01, NFR-03, NFR-04.
