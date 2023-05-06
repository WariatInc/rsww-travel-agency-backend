from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy.dialects.postgresql as psql
from sqlalchemy.orm import Session

from src.reservation_read_store.domain.ports import (
    IReservationReadStoreRepository,
)
from src.reservation_read_store.infrastructure.storage.models import (
    ReservationReadStore,
)
from src.utils import get_current_time

if TYPE_CHECKING:
    from src.consts import ReservationState


class ReservationReadStoreRepository(IReservationReadStoreRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def upsert_reservation_read_store(
        self, reservation_id: UUID, state: "ReservationState"
    ) -> None:
        t = ReservationReadStore.__table__
        stmt = psql.insert(t).values(
            _created=get_current_time(),
            _updated=get_current_time(),
            reservation_id=reservation_id,
            state=state,
        )
        stmt = stmt.on_conflict_do_update(
            constraint=t.primary_key,
            set_=dict(
                state=stmt.excluded.state,
                _updated=stmt.excluded._updated,
            ),
        )

        self._session.execute(stmt)

    def delete_reservation_from_read_store(self, reservation_id: UUID) -> None:
        self._session.query(ReservationReadStore).filter(
            ReservationReadStore.reservation_id == reservation_id
        ).delete()
