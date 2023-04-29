from typing import TYPE_CHECKING

from src.offer.domain.dtos import OfferDto

if TYPE_CHECKING:
    from src.offer.infrastructure.storage.models import Offer


def offer_dto_factory(offer: "Offer") -> OfferDto:
    return OfferDto(
        id=offer.id,
        arrival_date=offer.arrival_date,
        departure_date=offer.departure_date,
        departure_city=offer.departure_city,
        transport=offer.transport,
        number_of_kids=offer.number_of_kids,
        number_of_adults=offer.number_of_adults,
        room_type=offer.room_type,
        available=offer.available,
        tour_id=offer.tour_id,
    )
