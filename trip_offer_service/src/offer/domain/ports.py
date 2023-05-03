from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.offer.infrastructure.queries.search import SearchOptions
from src.offer.infrastructure.storage.offer import Offer, SimpleOffer


class IGetOfferQuery(ABC):
    @abstractmethod
    def get_offer(offer_id: UUID) -> Optional[Offer]:
        raise NotImplementedError()


class ISearchOfferQuery(ABC):
    @abstractmethod
    def search_offers(options: SearchOptions) -> list[SimpleOffer]:
        raise NotImplementedError()

    @abstractmethod
    def count_offers(options: SearchOptions) -> int:
        raise NotImplementedError()
