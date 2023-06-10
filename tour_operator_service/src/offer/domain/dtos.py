from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from src.consts import Transport

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


@dataclass
class TourDto:
    id: UUID
    operator: UUID
    hotel: str
    country: str
    departure_city: str
    description: str
    thumbnail_url: str
    arrival_date: datetime
    departure_date: datetime
    transport: Transport
    average_night_cost: float
    average_flight_cost: float
