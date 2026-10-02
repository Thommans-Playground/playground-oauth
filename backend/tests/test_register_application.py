import pytest

from app.application.use_cases.register_application import (
    RegisterApplication,
    RegisterApplicationCommand,
)
from app.infrastructure.adapters.persistence.in_memory_application_repository import (
    InMemoryApplicationRepository,
)


class StubIdGenerator:
    def __init__(self, value: str) -> None:
        self._value = value

    def new_id(self) -> str:
        return self._value


def test_register_application_persists_entity() -> None:
    repository = InMemoryApplicationRepository()
    use_case = RegisterApplication(repository=repository, id_generator=StubIdGenerator("client-123"))

    application = use_case.execute(RegisterApplicationCommand(client_name="My OAuth Client"))

    assert application.client_id == "client-123"
    assert repository.get("client-123") == application


def test_register_application_rejects_blank_name() -> None:
    repository = InMemoryApplicationRepository()
    use_case = RegisterApplication(repository=repository, id_generator=StubIdGenerator("client-123"))

    with pytest.raises(ValueError, match="must not be blank"):
        use_case.execute(RegisterApplicationCommand(client_name="   "))
