from typing import TYPE_CHECKING, Optional
from uuid import UUID

from src.infrastructure.storage import ReadOnlySessionFactory
from src.reservation_read_store.domain.factories import reservation_dto_factory
from src.reservation_read_store.domain.ports import IReservationReadStoreView
from src.reservation_read_store.infrastructure.storage.models import (
    ReservationReadStore,
)

if TYPE_CHECKING:
    from src.reservation_read_store.domain.dtos import ReservationDto


class ReservationReadStoreView(IReservationReadStoreView):
    def __init__(self, session_factory: ReadOnlySessionFactory) -> None:
        self._session = session_factory.create_session()

    def get_reservation(
        self, reservation_id: UUID
    ) -> Optional["ReservationDto"]:
        if (
            reservation := self._session.query(ReservationReadStore)
            .filter(ReservationReadStore.reservation_id == reservation_id)
            .one_or_none()
        ):
            return reservation_dto_factory(reservation)
