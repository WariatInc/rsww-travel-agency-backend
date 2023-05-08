from dataclasses import dataclass
from uuid import UUID


@dataclass
class ActorDto:
    gid: UUID
    first_name: str
    last_name: str
    email: str
