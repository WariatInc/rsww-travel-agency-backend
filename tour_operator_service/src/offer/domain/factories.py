from typing import TYPE_CHECKING

from src.offer.domain.dtos import OfferDto

if TYPE_CHECKING:
    from src.offer.infrastructure.storage.models import Offer


def offer_dto_factory(offer: "Offer") -> OfferDto:
    return OfferDto(
        id=offer.id,
        number_of_kids=offer.number_of_kids,
        number_of_adults=offer.number_of_adults,
        room_type=offer.room_type,
        available=offer.available,
        tour_id=offer.tour_id,
        all_inclusive=offer.all_inclusive,
        breakfast=offer.breakfast,
    )
