# UC-01: Register with Email and Password

- **Primary Actor:** Visitor (no account yet)
- **Trigger:** The actor submits an email address and a password to create an account.
- **Preconditions:** No account already exists with that email address.

## Main Success Scenario

Each step is tagged `[UC-01.n]` on its corresponding message in
`uc-01-register-with-password.puml`.

1. *Driving adapter* (REST `POST /auth/register`) receives the request and maps it to a
   `RegisterWithPasswordInput` DTO.
2. *Application* (`RegisterWithPassword` use case) receives the DTO.
3. *Application* calls the `UserRepository` port's `get_by_email()` and confirms no user
   exists for that email.
4. *Domain* constructs a `User` aggregate: validates `Email` (format) and the raw password
   (policy: minimum length, not a known-breached/trivial password), hashes it via the
   `PasswordHasher` port into a `PasswordCredential`, and assigns a `UserId` (via the
   `IdGenerator` port).
5. *Application* passes the new `User` to the `UserRepository` port's `save()`.
6. *Driven adapter* (`PostgresUserRepository`) persists the user.
7. *Application* returns the created `User` (never the password or its hash) to the
   driving adapter, which maps it to a REST response body.

## Extensions / Exceptions

- **3a. Email already registered:** Application returns an application-level "already
  exists" error; the driving adapter maps it to HTTP 409.
- **4a. Invalid email format, or password fails policy:** Domain raises a validation
  error; application catches it and returns an application-level validation error (not the
  raw domain exception) to the driving adapter, which maps it to HTTP 422 — no domain
  exception leaks past the use-case boundary.

## Postconditions

- A new `User` exists in the repository, retrievable by `UserId` or `Email`, with a
  `PasswordCredential` set and no linked social identities.
- No session is created by registration alone — the actor must log in afterward (UC-02).

## Related Requirements

FR-01, NFR-01, NFR-02.
