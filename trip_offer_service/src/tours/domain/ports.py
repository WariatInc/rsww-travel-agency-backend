from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import UUID

from src.tours.domain.dtos import SearchOptions, TourDto


class IToursView(ABC):
    @abstractmethod
    def search(self, options: SearchOptions) -> tuple[list[TourDto], int]:
        raise NotImplementedError

    @abstractmethod
    def search_options(self) -> dict[str, Any]:
        raise NotImplementedError


class IQuerySearchTours(ABC):
    @abstractmethod
    def __call__(self, options: SearchOptions) -> tuple[list[TourDto], int]:
        raise NotImplementedError


class IQueryCountTours(ABC):
    @abstractmethod
    def __call__(self, options: SearchOptions) -> int:
        raise NotImplementedError


class IQuerySearchOptions(ABC):
    @abstractmethod
    def __call__(self) -> dict[str, Any]:
        raise NotImplementedError


class ITourView(ABC):
    @abstractmethod
    def get(self, tour_id: UUID) -> Optional[TourDto]:
        raise NotImplementedError


class IGetTourQuery(ABC):
    @abstractmethod
    def get(self, tour_id: UUID) -> TourDto:
        raise NotImplementedError


class ITourRepository(ABC):
    @abstractmethod
    def upsert_tour(self, tour_id: UUID, **upsert_kwargs) -> None:
        raise NotImplementedError


class IUpsertTourCommand(ABC):
    @abstractmethod
    def __call__(self, **kwargs) -> None:
        raise NotImplementedError
