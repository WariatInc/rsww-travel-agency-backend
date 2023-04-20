from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.consts import ReservationState
from src.reservation.domain.dtos import ReservationDto


class IReservationRepository(ABC):
    @abstractmethod
    def create_reservation(
        self, user_id: UUID, offer_id: UUID
    ) -> ReservationDto:
        raise NotImplementedError

    @abstractmethod
    def set_reservation_state(
        self, reservation_id: UUID, state: ReservationState
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_reservation(
        self, reservation_id: UUID
    ) -> Optional[ReservationDto]:
        raise NotImplementedError

    @abstractmethod
    def check_if_offer_reservation_exits_in_pending_or_accepted_state(
        self, offer_id: UUID
    ) -> bool:
        raise NotImplementedError


class IReservationUnitOfWork(ABC):
    reservation_repository: IReservationRepository

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class ICreateReservationCommand(ABC):
    @abstractmethod
    def __call__(self, offer_id: UUID) -> None:
        raise NotImplementedError


class ICancelReservationCommand(ABC):
    @abstractmethod
    def __call__(self, reservation_id: UUID) -> None:
        raise NotImplementedError


class IReservationListView(ABC):
    @abstractmethod
    def get_list(self, user_id: UUID) -> list[ReservationDto]:
        raise NotImplementedError


class IGetUserReservationsQuery(ABC):
    @abstractmethod
    def get(self) -> list[ReservationDto]:
        raise NotImplementedError
