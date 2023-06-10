from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.consts import SortOrder, TourSort, TransportType


@dataclass
class TourDto:
    id: UUID
    country: str
    city: str
    hotel: str
    description: str
    thumbnail_url: str
    arrival_date: datetime
    departure_date: datetime
    transport: TransportType
    departure_city: str
    lowest_price: Optional[float] = None


@dataclass
class SearchOptions:
    page: int = 1
    page_size: int = 25
    country: Optional[str] = None
    operator: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    transport: Optional[str] = None
    adults: Optional[str] = None
    kids: Optional[str] = None
    departure_city: Optional[str] = None
    sort_by: TourSort = TourSort.arrival_date
    sort_order: SortOrder = SortOrder.asc
