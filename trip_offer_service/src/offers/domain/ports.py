from abc import ABC, abstractmethod
from typing import Any

from src.offers.domain.dtos import SearchOptions
from src.offer.domain.dtos import OfferDto


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
