# UC-04: Log Out

- **Primary Actor:** User (holds a session cookie)
- **Trigger:** The actor requests to log out.
- **Preconditions:** A session may or may not still be valid for the cookie presented.

## Main Success Scenario

Each step is tagged `[UC-04.n]` on its corresponding message in `uc-04-logout.puml`.

1. *Driving adapter* (REST `POST /auth/logout`) reads the `SessionId` from the session
   cookie and maps it to a `LogOut` input.
2. *Application* (`LogOut` use case) receives the `SessionId`.
3. *Application* calls the `SessionRepository` port's `delete()`.
4. *Driven adapter* (`RedisSessionRepository`) removes the session.
5. *Application* confirms the deletion to the driving adapter, which clears the session
   cookie and returns the response.

## Extensions / Exceptions

- **3a. No session exists for that id** (already logged out, or expired): Treated as
  already-logged-out — the operation is idempotent, still mapped to HTTP 204.

## Postconditions

- The session no longer exists in the repository.
- The actor's session cookie is cleared.

## Related Requirements

FR-08, NFR-01, NFR-04.
