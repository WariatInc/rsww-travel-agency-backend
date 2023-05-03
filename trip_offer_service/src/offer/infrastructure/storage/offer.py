from dataclasses import dataclass, fields
from typing import Any
from uuid import UUID


@dataclass
class Offer:
    offer_id: UUID
    tour_id: UUID
    operator: str
    country: str
    city: str
    description: str
    thumbnail_url: str
    arrival_date: str
    departure_date: str
    city: str
    transport: str
    number_of_adults: int
    number_of_kids: int
    room_type: str
    is_available: str

@dataclass
class SimpleOffer:
    offer_id: UUID
    tour_id: UUID
    operator: str
    country: str
    city: str
    thumbnail_url: str
    arrival_date: str
    departure_date: str
    is_available: str
