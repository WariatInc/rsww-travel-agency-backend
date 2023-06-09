from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.reservation.domain.dtos import (
    ReservationDetailsDto,
    ReservationDto,
    ReservationEventDashboardDto,
)
from src.user.domain.ports import IUserRepository


class IReservationRepository(ABC):
    @abstractmethod
    def create_reservation(
        self,
        user_id: UUID,
        offer_id: UUID,
        kids_up_to_3: int,
        kids_up_to_10: int,
    ) -> ReservationDetailsDto:
        raise NotImplementedError

    @abstractmethod
    def update_reservation(
        self, reservation_id: UUID, **update_kwargs
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_reservation(
        self, reservation_id: UUID
    ) -> Optional[ReservationDetailsDto]:
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
    def __call__(
        self,
        user_gid: UUID,
        offer_id: UUID,
        kids_up_to_3: int,
        kids_up_to_10: int,
    ) -> "ReservationDetailsDto":
        raise NotImplementedError


class ICancelReservationCommand(ABC):
    @abstractmethod
    def __call__(self, user_gid: UUID, reservation_id: UUID) -> None:
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
    ) -> Optional[ReservationDetailsDto]:
        raise NotImplementedError


class IGetReservationQuery(ABC):
    @abstractmethod
    def get(
        self, user_gid: UUID, reservation_id: UUID
    ) -> ReservationDetailsDto:
        raise NotImplementedError


class IGetUserReservationsQuery(ABC):
    @abstractmethod
    def get(self, user_gid: UUID) -> list[ReservationDto]:
        raise NotImplementedError


class IDeleteRejectedReservationCommand(ABC):
    @abstractmethod
    def __call__(self, user_gid: UUID, reservation_id: UUID) -> None:
        raise NotImplementedError


class IReservationEventDashboardRepository(ABC):
    @abstractmethod
    def add_reservation_event(
        self,
        reservation_event_id: UUID,
        timestamp: datetime,
        reservation_dto: ReservationDto,
    ) -> None:
        raise NotImplementedError


class IReservationEventDashboardUnitOfWork(ABC):
    reservation_event_dashboard_repository: IReservationEventDashboardRepository
    reservation_repository: IReservationRepository

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class IUpdateReservationEventDashboardCommand(ABC):
    @abstractmethod
    def __call__(
        self,
        reservation_event_id: UUID,
        reservation_id: UUID,
        timestamp: datetime,
    ) -> None:
        raise NotImplementedError


class IReservationEventDashboardListView(ABC):
    @abstractmethod
    def get_list(
        self, page: int, size: int
    ) -> tuple[list[ReservationEventDashboardDto], int]:
        raise NotImplementedError


class IGetReservationEventDashboardListQuery(ABC):
    @abstractmethod
    def get(
        self, page: int, size: int
    ) -> tuple[list[ReservationEventDashboardDto], int]:
        raise NotImplementedError


class IReservationsToCancelView(ABC):
    @abstractmethod
    def get(self) -> list[ReservationDto]:
        raise NotImplementedError
