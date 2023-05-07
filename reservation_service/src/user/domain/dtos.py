from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserDto:
    id: UUID
