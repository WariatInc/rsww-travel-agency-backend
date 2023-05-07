from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.reservation.domain.dtos import ReservationDto
from src.user.domain.ports import IUserRepository


class IReservationRepository(ABC):
    @abstractmethod
    def create_reservation(
        self, user_id: UUID, offer_id: UUID
    ) -> ReservationDto:
        raise NotImplementedError

    @abstractmethod
    def update_reservation(
        self, reservation_id: UUID, **update_kwargs
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_reservation(
        self, reservation_id: UUID
    ) -> Optional[ReservationDto]:
        raise NotImplementedError

    @abstractmethod
    def check_if_offer_reservation_exits_in_pending_accepted_or_paid_state(
        self, offer_id: UUID
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_reservation(self, reservation_id: UUID) -> None:
        raise NotImplementedError


class IReservationUnitOfWork(ABC):
    reservation_repository: IReservationRepository
    user_repository: IUserRepository

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class ICreateReservationCommand(ABC):
    @abstractmethod
    def __call__(self, user_gid: UUID, offer_id: UUID) -> "ReservationDto":
        raise NotImplementedError


class ICancelReservationCommand(ABC):
    @abstractmethod
    def __call__(
        self, user_gid: UUID, reservation_id: UUID
    ) -> "ReservationDto":
        raise NotImplementedError


class IUpdateReservationCommand(ABC):
    @abstractmethod
    def __call__(self, reservation_id: UUID, **update_kwargs) -> None:
        raise NotImplementedError


class IReservationListView(ABC):
    @abstractmethod
    def get_list(self, user_gid: UUID) -> list[ReservationDto]:
        raise NotImplementedError


class IReservationView(ABC):
    @abstractmethod
    def get(
        self, user_id: UUID, reservation_id: UUID
    ) -> Optional[ReservationDto]:
        raise NotImplementedError


class IGetReservationQuery(ABC):
    @abstractmethod
    def get(self, user_gid: UUID, reservation_id: UUID) -> ReservationDto:
        raise NotImplementedError


class IGetUserReservationsQuery(ABC):
    @abstractmethod
    def get(self, user_gid: UUID) -> list[ReservationDto]:
        raise NotImplementedError


class IDeleteRejectedReservationCommand(ABC):
    @abstractmethod
    def __call__(self, user_gid: UUID, reservation_id: UUID) -> None:
        raise NotImplementedError
