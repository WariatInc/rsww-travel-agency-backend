from typing import Any, Optional
from uuid import UUID

from src.consts import RejectionReason, ReservationState
from src.domain.events import DomainEvent


class OfferChangedEvent(DomainEvent):
    offer_id: UUID
    details: dict[str, Any]


class ReservationCheckedEvent(DomainEvent):
    reservation_id: UUID
    reservation_state: ReservationState
    reason: Optional[RejectionReason]
