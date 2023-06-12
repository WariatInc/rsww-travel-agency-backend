from abc import ABC, abstractmethod
from typing import Any


class IEnrichReservationsWithOffersDataCommand(ABC):
    @abstractmethod
    def __call__(
        self, reservations: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        raise NotImplementedError


class IGetUsersPreferencesQuery(ABC):
    @abstractmethod
    def get(self, offers_ids: list[str]) -> dict[str, list[str]]:
        raise NotImplementedError
