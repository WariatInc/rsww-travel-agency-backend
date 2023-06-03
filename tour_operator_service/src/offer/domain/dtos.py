from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from src.consts import RoomType


@dataclass
class OfferDto:
    id: UUID
    number_of_adults: int
    number_of_kids: int
    room_type: "RoomType"
    available: bool
    tour_id: UUID
    all_inclusive: bool
    breakfast: bool
