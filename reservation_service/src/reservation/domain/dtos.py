from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.consts import CancelReason, ReservationState
from src.user.domain.dtos import UserDto


@dataclass
class ReservationDto:
    id: UUID
    state: ReservationState
    offer_id: UUID
    user: Optional[UserDto]
    rejection_reason: Optional[str]
    cancel_reason: Optional[CancelReason]
    price: Optional[float]


@dataclass
class ReservationDetailsDto(ReservationDto):
    kids_up_to_3: int
    kids_up_to_10: int


@dataclass
class ReservationEventDashboardDto:
    id: UUID
    reservation_id: UUID
    offer_id: UUID
    state: ReservationState
    timestamp: datetime
