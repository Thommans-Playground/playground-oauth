# playground-oauth

Monorepo bootstrap with:

- **Frontend**: Next.js (TypeScript, Tailwind CSS, shadcn/ui baseline)
- **Backend**: FastAPI (Python) with DDD + Hexagonal architecture (ports and adapters)
- **Data services**: PostgreSQL + Redis
- **Containers**: Dockerfiles for frontend/backend and orchestration via Docker Compose

## Structure

- `/frontend` Next.js app
- `/backend` FastAPI app
  - `domain`: entities + repository interfaces
  - `application`: use cases + ports
  - `infrastructure`: adapters (HTTP + persistence)

## Local run (Docker Compose)

```bash
docker compose up --build
```

Endpoints:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- OpenAPI docs: `http://localhost:8000/docs`

## Backend tests

```bash
cd backend
pip install -e .[dev]
pytest
```
