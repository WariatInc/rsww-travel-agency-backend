from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.offer.domain.dtos import OfferDto, OfferViewDto
from src.offers.domain.dtos import OfferEnrichmentDataDto, SearchOptions


class IOffersView(ABC):
    @abstractmethod
    def count(self, options: SearchOptions) -> int:
        raise NotImplementedError

    @abstractmethod
    def search(self, options: SearchOptions) -> list[OfferDto]:
        raise NotImplementedError

    @abstractmethod
    def search_options(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def inspect(self, offer_id: UUID) -> OfferViewDto:
        raise NotImplementedError

    def get_offer_views_by_offer_ids(self, offer_ids: list[str]) -> list[OfferViewDto]:
        raise NotImplementedError


class IOfferRepository(ABC):
    @abstractmethod
    def upsert_offer(self, offer_id: UUID, **upsert_kwargs) -> None:
        raise NotImplementedError


class IQuerySearchOffers(ABC):
    @abstractmethod
    def __call__(self, options: SearchOptions) -> list[OfferDto]:
        raise NotImplementedError


class IQueryCountOffers(ABC):
    @abstractmethod
    def __call__(self, options: SearchOptions) -> int:
        raise NotImplementedError


class IQuerySearchOptions(ABC):
    @abstractmethod
    def __call__(self) -> dict[str, Any]:
        raise NotImplementedError


class IQueryOffer(ABC):
    @abstractmethod
    def __call__(self, offer_id: UUID) -> OfferViewDto:
        raise NotImplementedError


class IGetOfferEnrichmentDataQuery(ABC):
    @abstractmethod
    def get(self, offer_ids: list[UUID]) -> dict[UUID, OfferEnrichmentDataDto]:
        raise NotImplementedError


class IUpdateOffer(ABC):
    @abstractmethod
    def __call__(self, offer_id: UUID, **fields) -> None:
        raise NotImplementedError
