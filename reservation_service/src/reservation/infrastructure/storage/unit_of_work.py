from src.infrastructure.storage import SessionFactory
from src.reservation.domain.ports import IReservationUnitOfWork
from src.reservation.infrastructure.storage.repository import (
    ReservationRepository,
)


class ReservationUnitOfWork(IReservationUnitOfWork):
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> None:
        self._session = self._session_factory.create_session()
        self.reservation_repository = ReservationRepository(self._session)

    def __exit__(self, **kwargs) -> None:
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
