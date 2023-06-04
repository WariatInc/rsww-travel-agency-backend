from src.offer_old.domain.dtos import OfferDto
from src.offer_old.infrastructure.storage.documents import Offer


def offer_dto_factory(offer: Offer) -> OfferDto:
    return OfferDto(**offer)
