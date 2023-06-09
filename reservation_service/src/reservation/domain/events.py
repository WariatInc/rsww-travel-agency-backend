from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from src.consts import ReservationState
from src.domain.events import DomainEvent, Event


@dataclass
class ReservationCreatedEvent(DomainEvent):
    offer_id: UUID
    reservation_id: UUID
    kids_up_to_3: int
    kids_up_to_10: int


@dataclass
class ReservationUpdatedEvent(DomainEvent):
    reservation_id: UUID
    details: dict[str, Any]


@dataclass
class ReservationCancelledEvent(DomainEvent):
    offer_id: UUID


@dataclass
class ReservationDeletedEvent(DomainEvent):
    reservation_id: UUID


@dataclass
class ReservationCheckedEvent(Event):
    reservation_id: UUID
    reservation_state: ReservationState
    rejection_reason: Optional[str]
    _price: Optional[str]

    @classmethod
    def from_rabbitmq_message(
        cls, message: dict[str, str]
    ) -> "ReservationCheckedEvent":
        return cls(
            id=UUID(message.get("id")),
            time=datetime.fromisoformat(message.get("time")),
            type=message.get("type"),
            reservation_id=UUID(message.get("reservation_id")),
            reservation_state=ReservationState(
                message.get("reservation_state")
            ),
            rejection_reason=message.get("reason"),
            _price=message.get("price"),
        )

    @property
    def price(self) -> Optional[float]:
        if _price := self._price:
            return float(_price)


@dataclass
class ReservationEventDashboardUpdate(DomainEvent):
    reservation_id: UUID

    @classmethod
    def from_rabbitmq_message(
        cls, message: dict[str, str]
    ) -> "ReservationEventDashboardUpdate":
        return cls(
            id=UUID(message.get("id")),
            time=datetime.fromisoformat(message.get("time")),
            type=message.get("type"),
            reservation_id=UUID(message.get("reservation_id")),
        )
