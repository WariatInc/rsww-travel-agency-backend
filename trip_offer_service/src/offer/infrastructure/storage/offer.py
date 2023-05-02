from typing import Any
from dataclasses import dataclass, fields
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
    departure_city: str
    transport: str
    number_of_adults: int
    number_of_kids: int
    room_type: str
    is_available: str

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> "Offer":
        return Offer(**{
            field.name: json_data[field.name]
            for field in fields(Offer) 
        })

    def to_json(self) -> dict[str, Any]:
        return {
            field.name: getattr(self, field.name)
            for field in fields(Offer) 
        }


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
    
    @staticmethod
    def from_json(json_data: dict[str, Any]) -> "SimpleOffer":
        return SimpleOffer(**{
            field.name: json_data[field.name]
            for field in fields(SimpleOffer) 
        })

    def to_json(self) -> dict[str, Any]:
        return {
            field.name: getattr(self, field.name)
            for field in fields(SimpleOffer) 
        }
