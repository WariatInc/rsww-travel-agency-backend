from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import UUID

from src.offer.domain.dtos import OfferDto, SearchOptions, SimpleOfferDto


class IGetOfferQuery(ABC):
    @abstractmethod
    def get_offer(self, offer_id: UUID) -> Optional[OfferDto]:
        raise NotImplementedError()


class ISearchOfferQuery(ABC):
    @abstractmethod
    def search_offers(self, options: SearchOptions) -> list[SimpleOfferDto]:
        raise NotImplementedError()

    @abstractmethod
    def count_offers(self, options: SearchOptions) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_search_options(self) -> dict[str, Any]:
        raise NotImplementedError()


class IOfferRepository(ABC):
    @abstractmethod
    def upsert_offer(self, offer_id: UUID, **upsert_kwargs) -> None:
        raise NotImplementedError
