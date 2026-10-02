from abc import ABC, abstractmethod

from app.domain.entities.application import Application


class ApplicationRepository(ABC):
    @abstractmethod
    def add(self, application: Application) -> Application:
        raise NotImplementedError

    @abstractmethod
    def get(self, client_id: str) -> Application | None:
        raise NotImplementedError
