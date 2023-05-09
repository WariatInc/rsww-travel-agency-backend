from typing import Optional
from uuid import UUID

import sqlalchemy as sqla
from src.consts import ReservationState
from src.infrastructure.storage import ReadOnlySessionFactory
from src.reservation.domain.dtos import ReservationDetailsDto, ReservationDto
from src.reservation.domain.factories import (reservation_details_dto_factory,
                                              reservation_dto_factory)
from src.reservation.domain.ports import IReservationListView, IReservationView
from src.reservation.infrastructure.storage.models import Reservation


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
