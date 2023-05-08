from dataclasses import dataclass
from uuid import UUID

from src.consts import ReservationState


@dataclass
class ReservationDto:
    reservation_id: UUID
    state: ReservationState
