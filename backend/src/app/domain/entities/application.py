from dataclasses import dataclass


@dataclass(frozen=True)
class Application:
    client_id: str
    client_name: str
