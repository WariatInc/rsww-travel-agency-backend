from dataclasses import dataclass
from uuid import UUID

from src.domain.events import DomainEvent


@dataclass
class ReservationCreatedEvent(DomainEvent):
    offer_id: UUID
    reservation_id: UUID


@dataclass
class ReservationCancelledEvent(DomainEvent):
    offer_id: UUID
