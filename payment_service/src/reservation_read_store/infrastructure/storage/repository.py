from uuid import UUID

import sqlalchemy.dialects.postgresql as psql
from sqlalchemy.orm import Session
from src.consts import RESERVATION_READ_STORE_COLUMNS
from src.reservation_read_store.domain.ports import \
    IReservationReadStoreRepository
from src.reservation_read_store.infrastructure.storage.models import \
    ReservationReadStore
from src.utils import get_current_time


class ReservationReadStoreRepository(IReservationReadStoreRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def upsert_reservation_read_store(
        self, reservation_id: UUID, **upsert_kwargs
    ) -> None:
        filtered_kwargs = {
            key: value
            for key, value in upsert_kwargs.items()
            if key in RESERVATION_READ_STORE_COLUMNS
        }
        t = ReservationReadStore.__table__
        stmt = psql.insert(t).values(
            _created=get_current_time(),
            _updated=get_current_time(),
            reservation_id=reservation_id,
            **filtered_kwargs,
        )
        stmt = stmt.on_conflict_do_update(
            constraint=t.primary_key,
            set_=dict(_updated=stmt.excluded._updated, **filtered_kwargs),
        )

        self._session.execute(stmt)

    def delete_reservation_from_read_store(self, reservation_id: UUID) -> None:
        self._session.query(ReservationReadStore).filter(
            ReservationReadStore.reservation_id == reservation_id
        ).delete()
