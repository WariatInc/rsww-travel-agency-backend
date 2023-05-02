from abc import ABC, abstractmethod
from uuid import UUID

from src.offer.infrastructure.storage.offer import Offer, SimpleOffer
from src.offer.infrastructure.queries.search import SearchOptions


class IGetOfferQuery(ABC):
    @abstractmethod
    def get_offer(offer_id: UUID) -> Offer:
        raise NotImplemented


class ISearchOfferQuery(ABC):
    @abstractmethod
    def search_offers(options: SearchOptions) -> list[SimpleOffer]:
        raise NotImplemented
