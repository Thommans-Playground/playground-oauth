from dataclasses import dataclass

from app.application.ports.id_generator import IdGenerator
from app.domain.entities.application import Application
from app.domain.repositories.application_repository import ApplicationRepository


@dataclass
class RegisterApplicationCommand:
    client_name: str


class RegisterApplication:
    def __init__(self, repository: ApplicationRepository, id_generator: IdGenerator) -> None:
        self._repository = repository
        self._id_generator = id_generator

    def execute(self, command: RegisterApplicationCommand) -> Application:
        client_name = command.client_name.strip()
        if not client_name:
            raise ValueError("client_name must not be blank")

        application = Application(
            client_id=self._id_generator.new_id(),
            client_name=client_name,
        )
        return self._repository.add(application)
