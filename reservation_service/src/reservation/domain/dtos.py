from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.consts import ReservationState


@dataclass
class ReservationDto:
    id: UUID
    state: ReservationState
    offer_id: UUID
    user_id: UUID
    rejection_reason: Optional[str]


@dataclass
class ReservationDetailsDto(ReservationDto):
    kids_up_to_3: int
    kids_up_to_10: int
    price: float
