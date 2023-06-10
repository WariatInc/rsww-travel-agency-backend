from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.consts import OfferSort, RoomType, SortOrder


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
    sort_by: Optional[OfferSort] = None
    sort_order: SortOrder = SortOrder.asc


@dataclass
class OfferEnrichmentDataDto:
    hotel: str
    country: str
    city: str
    thumbnail_url: str
    arrival_date: datetime
    departure_date: datetime
