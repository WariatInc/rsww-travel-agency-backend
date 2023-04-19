from dataclasses import dataclass
from uuid import UUID


@dataclass
class ActorDto:
    id: UUID
    gid: UUID
