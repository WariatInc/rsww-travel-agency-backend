from src.infrastructure.storage import SessionFactory
from src.reservation_read_store.domain.ports import (
    IReservationReadStoreUnitOfWork,
)
from src.reservation_read_store.infrastructure.storage.repository import (
    ReservationReadStoreRepository,
)


class ReservationReadStoreUnitOfWork(IReservationReadStoreUnitOfWork):
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> None:
        self._session = self._session_factory.create_session()
        self.reservation_read_store_repository = (
            ReservationReadStoreRepository(self._session)
        )

    def __exit__(self, *args) -> None:
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
