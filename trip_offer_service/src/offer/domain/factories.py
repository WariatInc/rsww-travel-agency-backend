from src.offer.domain.dtos import OfferDto
from src.offer.infrastructure.storage.documents import Offer


def offer_dto_factory(offer: Offer) -> OfferDto:
    return OfferDto(**offer)
