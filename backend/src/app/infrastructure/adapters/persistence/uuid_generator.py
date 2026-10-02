import uuid

from app.application.ports.id_generator import IdGenerator


class UuidGenerator(IdGenerator):
    def new_id(self) -> str:
        return str(uuid.uuid4())
