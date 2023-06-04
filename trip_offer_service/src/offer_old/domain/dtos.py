from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.consts import RoomType, TransportType


@dataclass
class OfferDto:
    offer_id: UUID
    tour_id: UUID
    operator: str
    country: str
    city: str
    description: str
    thumbnail_url: str
    arrival_date: datetime
    departure_date: datetime
    departure_city: Optional[str]
    city: str
    transport: TransportType
    number_of_adults: int
    number_of_kids: int
    room_type: RoomType
    is_available: bool


@dataclass
class SimpleOfferDto:
    offer_id: UUID
    tour_id: UUID
    operator: str
    country: str
    city: str
    thumbnail_url: str
    arrival_date: datetime
    departure_date: datetime
    departure_city: Optional[str]
    transport: TransportType
    number_of_adults: int
    number_of_kids: int
    room_type: RoomType
    is_available: bool
    price: Optional[float] = None


@dataclass
class SearchOptions:
    page: int = 1
    page_size: int = 25
    operator: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    transport: Optional[str] = None
    adults: Optional[str] = None
    kids: Optional[str] = None
    room: Optional[str] = None
