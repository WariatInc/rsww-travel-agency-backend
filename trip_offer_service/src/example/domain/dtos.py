from dataclasses import dataclass
from uuid import UUID


@dataclass
class ExampleDto:
    uniq_id: UUID
    title: str
    author: str
