from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from src.consts import ReservationState
from src.domain.events import Event


@dataclass
class ReservationCreatedEvent(Event):
    reservation_id: UUID
    state: ReservationState

    @classmethod
    def from_rabbitmq_message(
        cls, message: dict[str, Any]
    ) -> "ReservationCreatedEvent":
        return cls(
            id=UUID(message.get("id")),
            time=datetime.fromisoformat(message.get("time")),
            type=message.get("type"),
            reservation_id=UUID(message.get("reservation_id")),
            state=ReservationState.pending,
        )


@dataclass
class ReservationUpdatedEvent(Event):
    reservation_id: UUID
    details: dict[str, Any]

    @classmethod
    def from_rabbitmq_message(
        cls, message: dict[str, Any]
    ) -> "ReservationUpdatedEvent":
        return cls(
            id=UUID(message.get("id")),
            time=datetime.fromisoformat(message.get("time")),
            type=message.get("type"),
            reservation_id=UUID(message.get("reservation_id")),
            details=message.get("details"),
        )


@dataclass
class ReservationDeletedEvent(Event):
    reservation_id: UUID

    @classmethod
    def from_rabbitmq_message(
        cls, message: dict[str, str]
    ) -> "ReservationDeletedEvent":
        return cls(
            id=UUID(message.get("id")),
            time=datetime.fromisoformat(message.get("time")),
            type=message.get("type"),
            reservation_id=UUID(message.get("reservation_id")),
        )
