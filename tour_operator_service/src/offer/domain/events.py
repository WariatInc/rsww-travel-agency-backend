from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from src.consts import RejectionReason, ReservationState
from src.domain.events import DomainEvent, Event


@dataclass
class OfferChangedEvent(DomainEvent):
    offer_id: UUID
    details: dict[str, Any]


@dataclass
class ReservationCheckedEvent(DomainEvent):
    reservation_id: UUID
    reservation_state: ReservationState
    reason: Optional[RejectionReason] = None


@dataclass
class ReservationCreatedEvent(Event):
    offer_id: UUID
    reservation_id: UUID

    @classmethod
    def from_rabbitmq_message(
        cls, message: dict[str, str]
    ) -> "ReservationCreatedEvent":
        return cls(
            id=UUID(message.get("id")),
            time=datetime.fromisoformat(message.get("time")),
            type=message.get("type"),
            offer_id=UUID(message.get("offer_id")),
            reservation_id=UUID(message.get("reservation_id")),
        )


@dataclass
class ReservationCancelledEvent(Event):
    offer_id: UUID

    @classmethod
    def from_rabbitmq_message(
        cls, message: dict[str, str]
    ) -> "ReservationCancelledEvent":
        return cls(
            id=UUID(message.get("id")),
            time=datetime.fromisoformat(message.get("time")),
            type=message.get("type"),
            offer_id=UUID(message.get("offer_id")),
        )
