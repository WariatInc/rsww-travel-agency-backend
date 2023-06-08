from typing import Any
from uuid import UUID

from src.consts import TransportType
from src.offer.domain.dtos import OfferViewDto


def offer_view_dto_factory(offer_view: dict[str, Any]) -> OfferViewDto:
    return OfferViewDto(
        offer_id=UUID(offer_view.get("id")),
        tour_id=UUID(offer_view.get("tour_id")),
        number_of_adults=offer_view.get("number_of_adults"),
        number_of_kids=offer_view.get("number_of_kids"),
        room_type=offer_view.get("room_type"),
        all_inclusive=offer_view.get("all_inclusive"),
        breakfast=offer_view.get("breakfast"),
        is_available=offer_view.get("is_available"),
        operator=offer_view["tour"].get("operator"),
        country=offer_view["tour"].get("country"),
        city=offer_view["tour"].get("city"),
        hotel=offer_view["tour"].get("hotel"),
        description=offer_view["tour"].get("description"),
        thumbnail_url=offer_view["tour"].get("thumbnail_url"),
        arrival_date=offer_view["tour"].get("arrival_date"),
        departure_date=offer_view["tour"].get("departure_date"),
        transport=TransportType(offer_view["tour"].get("transport")),
        departure_city=offer_view["tour"].get("departure_city"),
    )
