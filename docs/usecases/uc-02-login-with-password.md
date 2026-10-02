# UC-02: Log In with Email and Password

- **Primary Actor:** User
- **Trigger:** The actor submits an email address and a password.
- **Preconditions:** An account with that email may or may not exist.

## Main Success Scenario

Each step is tagged `[UC-02.n]` on its corresponding message in
`uc-02-login-with-password.puml`.

1. *Driving adapter* (REST `POST /auth/login`) receives the credentials and maps them to a
   `LoginWithPasswordInput` DTO.
2. *Application* (`LoginWithPassword` use case) receives the DTO.
3. *Application* calls the `UserRepository` port's `get_by_email()`.
4. *Application* verifies the submitted password against the stored `PasswordCredential`
   via the `PasswordHasher` port's `verify()`.
5. *Application* constructs a new `Session` aggregate (`SessionId` via `IdGenerator`,
   the matched `UserId`, `created_at`/`expires_at` via the `Clock` port, `auth_method` set
   to `password`).
6. *Application* passes the `Session` to the `SessionRepository` port's `save()`.
7. *Driven adapter* (`RedisSessionRepository`) persists the session.
8. *Application* returns the `Session` to the driving adapter, which sets an `HttpOnly`
   session cookie containing the `SessionId` (NFR-04) and returns the response.

## Extensions / Exceptions

- **3a. No account with that email:** Application returns a generic "invalid
  credentials" error — not "email not found," to avoid revealing which emails are
  registered — mapped to HTTP 401.
- **4a. Password does not match:** Application returns the same generic "invalid
  credentials" error, mapped to HTTP 401. Steps 3a and 4a are intentionally
  indistinguishable to the actor.

## Postconditions

- A `Session` exists, retrievable by `SessionId`, referencing the authenticated `User`.
- The response's `Set-Cookie` header carries that `SessionId`.

## Related Requirements

FR-02, FR-07, NFR-01, NFR-02, NFR-04.
