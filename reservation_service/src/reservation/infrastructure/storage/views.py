from datetime import datetime, timedelta
from math import ceil
from typing import Optional
from uuid import UUID

import sqlalchemy as sqla

from src.consts import ACCEPTED_RESERVATION_TIMEOUT, ReservationState
from src.infrastructure.storage import ReadOnlySessionFactory
from src.reservation.domain.dtos import (
    ReservationDetailsDto,
    ReservationDto,
    ReservationEventDashboardDto,
)
from src.reservation.domain.factories import (
    reservation_details_dto_factory,
    reservation_dto_factory,
    reservation_event_dashboard_dto_factory,
)
from src.reservation.domain.ports import (
    IReservationEventDashboardListView,
    IReservationListView,
    IReservationsToCancelView,
    IReservationView,
)
from src.reservation.infrastructure.storage.models import (
    Reservation,
    ReservationEventDashboard,
)


class ReservationListView(IReservationListView):
    def __init__(self, session_factory: ReadOnlySessionFactory) -> None:
        self._session = session_factory.create_session()

    def get_list(self, user_id: UUID) -> list[ReservationDto]:
        return [
            reservation_dto_factory(reservation)
            for reservation in self._session.query(Reservation)
            .filter(
                Reservation.user_id == user_id,
                Reservation.state != ReservationState.cancelled,
            )
            .order_by(sqla.desc(Reservation.created_at))
            .all()
        ]


class ReservationView(IReservationView):
    def __init__(self, session_factory: ReadOnlySessionFactory) -> None:
        self._session = session_factory.create_session()

    def get(
        self, user_id: UUID, reservation_id: UUID
    ) -> Optional[ReservationDetailsDto]:
        if (
            reservation := self._session.query(Reservation)
            .filter(
                Reservation.id == reservation_id,
                Reservation.user_id == user_id,
            )
            .one_or_none()
        ):
            return reservation_details_dto_factory(reservation)


class ReservationEventDashboardListView(IReservationEventDashboardListView):
    def __init__(self, session_factory: ReadOnlySessionFactory) -> None:
        self._session = session_factory.create_session()

    def get_list(
        self, page: int, size: int
    ) -> tuple[list[ReservationEventDashboardDto], int]:
        query = self._session.query(ReservationEventDashboard).order_by(
            sqla.desc(ReservationEventDashboard.timestamp)
        )
        return [
            reservation_event_dashboard_dto_factory(
                reservation_event_dashboard
            )
            for reservation_event_dashboard in query.offset((page - 1) * size)
            .limit(size)
            .all()
        ], ceil(query.count() / size)


class ReservationsToCancelView(IReservationsToCancelView):
    def __init__(self, session_factory: ReadOnlySessionFactory) -> None:
        self._session = session_factory.create_session()

    def get(self) -> list[ReservationDto]:
        return [
            reservation_dto_factory(reservation)
            for reservation in self._session.query(Reservation)
            .filter(
                Reservation.state == ReservationState.accepted,
                Reservation.updated_at
                < datetime.now()
                - timedelta(seconds=ACCEPTED_RESERVATION_TIMEOUT),
            )
            .all()
        ]
