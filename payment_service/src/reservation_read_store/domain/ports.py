from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from src.consts import ReservationState


class IReservationReadStoreRepository(ABC):
    @abstractmethod
    def upsert_reservation_read_store(
        self, reservation_id: UUID, state: "ReservationState"
    ) -> None:
        raise NotImplementedError


class IReservationReadStoreUnitOfWork(ABC):
    reservation_read_store_repository = IReservationReadStoreRepository

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class IReservationReadStoreSynchronizationCommand(ABC):
    @abstractmethod
    def __call__(
        self, reservation_id: UUID, state: "ReservationState"
    ) -> None:
        raise NotImplementedError
