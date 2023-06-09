from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.consts import RoomType, TransportType


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
    price: float


@dataclass
class OfferViewDto:
    offer_id: UUID
    tour_id: UUID
    number_of_adults: int
    number_of_kids: int
    room_type: RoomType
    all_inclusive: bool
    breakfast: bool
    is_available: bool
    operator: str
    country: str
    city: str
    hotel: str
    description: str
    thumbnail_url: str
    arrival_date: datetime
    departure_date: datetime
    transport: TransportType
    departure_city: str
    price: float
