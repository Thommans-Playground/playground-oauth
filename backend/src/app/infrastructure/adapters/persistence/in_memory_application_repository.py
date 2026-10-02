from app.domain.entities.application import Application
from app.domain.repositories.application_repository import ApplicationRepository


class InMemoryApplicationRepository(ApplicationRepository):
    def __init__(self) -> None:
        self._applications: dict[str, Application] = {}

    def add(self, application: Application) -> Application:
        self._applications[application.client_id] = application
        return application

    def get(self, client_id: str) -> Application | None:
        return self._applications.get(client_id)
