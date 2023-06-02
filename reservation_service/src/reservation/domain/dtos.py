from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.consts import ReservationState


@dataclass
class ReservationDto:
    id: UUID
    state: ReservationState
    offer_id: UUID
    user_id: UUID
    rejection_reason: Optional[str]
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
    time: datetime
