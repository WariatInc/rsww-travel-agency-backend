from dataclasses import dataclass
from typing import Any
from uuid import UUID

from src.domain.events import DomainEvent


@dataclass
class ExampleUpdatedEvent(DomainEvent):
    example_id: UUID
    details: dict[str, Any]
