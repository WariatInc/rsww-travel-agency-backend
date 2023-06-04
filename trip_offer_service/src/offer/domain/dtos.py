from dataclasses import dataclass
from uuid import UUID

from src.consts import RoomType


@dataclass
class OfferDto:
    id: UUID
    tour_id: UUID
    number_of_adults: int
    number_of_kids: int
    room_type: RoomType
    all_inclusive: bool
    breakfast: bool
    is_available: bool
