from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from src.domain.events import Event


@dataclass
class TourChangedEvent(Event):
    tour_id: UUID
    details: dict[str, Any]

    @classmethod
    def from_rabbitmq_message(
        cls, message: dict[str, Any]
    ) -> "TourChangedEvent":
        return cls(
            id=message.get("id"),
            time=datetime.fromisoformat(message.get("time")),
            type=message.get("type"),
            tour_id=UUID(message.get("tour_id")),
            details=message.get("details"),
        )
