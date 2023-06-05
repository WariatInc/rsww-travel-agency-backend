from abc import ABC, abstractmethod
from typing import Any

from src.tour.domain.dtos import TourDto
from src.tours.domain.dtos import SearchOptions


class IToursView(ABC):
    @abstractmethod
    def count(self, options: SearchOptions) -> int:
        raise NotImplementedError

    @abstractmethod
    def search(self, options: SearchOptions) -> list[TourDto]:
        raise NotImplementedError

    @abstractmethod
    def search_options(self) -> dict[str, Any]:
        raise NotImplementedError


class IQuerySearchTours(ABC):
    @abstractmethod
    def __call__(self, options: SearchOptions) -> list[TourDto]:
        raise NotImplementedError


class IQueryCountTours(ABC):
    @abstractmethod
    def __call__(self, options: SearchOptions) -> int:
        raise NotImplementedError


class IQuerySearchOptions(ABC):
    @abstractmethod
    def __call__(self) -> dict[str, Any]:
        raise NotImplementedError
