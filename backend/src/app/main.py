from fastapi import FastAPI

from app.application.use_cases.register_application import RegisterApplication
from app.infrastructure.adapters.http.router import build_router
from app.infrastructure.adapters.persistence.in_memory_application_repository import (
    InMemoryApplicationRepository,
)
from app.infrastructure.adapters.persistence.uuid_generator import UuidGenerator


def create_app() -> FastAPI:
    app = FastAPI(title="playground-oauth-backend")

    repository = InMemoryApplicationRepository()
    id_generator = UuidGenerator()
    register_application = RegisterApplication(repository=repository, id_generator=id_generator)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(build_router(register_application))
    return app


app = create_app()
