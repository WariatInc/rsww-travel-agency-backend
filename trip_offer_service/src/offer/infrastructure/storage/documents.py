from typing import TypedDict
from uuid import UUID

from src.consts import RoomType, TransportType


class Offer(TypedDict):
    """Document Representation"""

    offer_id: UUID
    tour_id: UUID
    operator: str
    city: str
    description: str
    thumbnail_url: str
    arrival_date: str
    departure_date: str
    city: str
    transport: TransportType
    number_of_adults: int
    number_of_kids: int
    room_type: RoomType
    is_available: bool
