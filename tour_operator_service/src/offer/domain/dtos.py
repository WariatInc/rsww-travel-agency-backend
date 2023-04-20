from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from datetime import date

    from src.consts import RoomType, Transport


@dataclass
class OfferDto:
    id: UUID
    arrival_date: "date"
    departure_date: "date"
    departure_city: str
    transport: "Transport"
    number_of_adults: int
    number_of_kids: int
    room_type: "RoomType"
    available: bool
    tour_id: UUID
