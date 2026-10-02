---
name: verify
description: Build/launch/drive recipe for verifying runtime behavior in this repo. Use when /verify needs a handle on a package and no more specific verifier applies yet.
---

# verify

This is a two-package monorepo (`backend/`, `frontend/`); split this into
`backend/.claude/skills/verify/` and `frontend/.claude/skills/verify/` once their
build/launch/drive mechanics genuinely diverge further (per the built-in `/verify`
skill's own rule) — not before.

There is no MCP adapter in this project (see `CLAUDE.md`) — REST is the only driving
adapter to drive.

## Backend (`backend/`)

### Build

```bash
cd backend && pip install -e .[dev]
```

### Drive — REST, via the real composition root

The composition root is `app.main.create_app()` — always go through it, not a
hand-assembled `FastAPI()` instance, so the actual adapter wiring is exercised:

```python
from fastapi.testclient import TestClient
from app.main import create_app

client = TestClient(create_app())
response = client.get("/health")
print(response.status_code, response.json())
```

Once the documented use cases exist (`docs/usecases/uc-01`..`uc-04`), the equivalent
drive calls are:

```python
client.post("/auth/register", json={"email": "a@example.com", "password": "..."})
client.post("/auth/login", json={"email": "a@example.com", "password": "..."})
client.get("/auth/oauth/google/start")  # expect a 3xx redirect; the callback leg
                                          # needs a real/stubbed provider response
client.post("/auth/logout")  # needs the session cookie from a prior login response
```

### Once a real server entrypoint is run (not just `TestClient`)

```bash
cd backend && uvicorn app.main:app --reload
```

Then `curl`/an HTTP client against `http://localhost:8000` exercises the actual running
process, including real cookie handling across requests — `TestClient` shares this but
some browser-only behavior (redirect following, `Secure` cookie rejection over plain HTTP)
only shows up against a real browser or `curl -v`.

## Frontend (`frontend/`)

### Build

```bash
cd frontend && npm install
```

### Drive

```bash
cd frontend && npm run dev   # http://localhost:3000
```

The frontend is currently the unmodified `create-next-app` starter — there is no login UI
to click through yet. Once one exists, drive it with the `claude-in-chrome` or built-in
browser skill against `localhost:3000`, not by reading the React source and assuming it
works.

## Gotchas found so far

- `docker-compose.yml` wires `DATABASE_URL`/`REDIS_URL` env vars into the backend
  container, but nothing in the code reads them yet — no persistence adapter exists (the
  backend is a clean slate besides the composition root and `IdGenerator`/`UuidGenerator`).
  Driving the app through Docker Compose today exercises the same bare `/health` check as
  running it directly; it does not yet exercise Postgres or Redis.

## Once Postgres/Redis adapters exist

Replace the in-memory assumption above: a `PostgresUserRepository`/`RedisSessionRepository`
drive needs an actual Postgres/Redis instance (`docker compose up postgres redis`, or a
disposable container) behind the composition root, not an in-memory fake — the whole point
of verifying is to exercise the real driven adapter, not bypass it.
