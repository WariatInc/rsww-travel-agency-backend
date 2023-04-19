from uuid import UUID

import sqlalchemy as sqla

from src.infrastructure.storage import ReadOnlySessionFactory
from src.reservation.domain.dtos import ReservationDto
from src.reservation.domain.factories import reservation_dto_factory
from src.reservation.domain.ports import IReservationListView
from src.reservation.infrastructure.storage.models import Reservation


class ReservationListView(IReservationListView):
    def __init__(self, session_factory: ReadOnlySessionFactory) -> None:
        self._session = session_factory.create_session()

    def get_list(self, user_id: UUID) -> list[ReservationDto]:
        return [
            reservation_dto_factory(reservation)
            for reservation in self._session.query(Reservation)
            .filter(Reservation.user_id == user_id)
            .order_by(sqla.desc(Reservation.created_at))
            .all()
        ]
