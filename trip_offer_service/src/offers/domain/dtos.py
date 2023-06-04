from dataclasses import dataclass
from uuid import UUID
from typing import Optional

from src.consts import RoomType


@dataclass
class SearchOptions:
    tour_id: UUID
    page: int = 1
    page_size: int = 25
    adults: Optional[int] = None
    kids: Optional[int] = None
    room_type: Optional[RoomType] = None
    all_inclusive: Optional[bool] = None
    breakfast: Optional[bool] = None
