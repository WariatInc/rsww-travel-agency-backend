from src.infrastructure.storage import SessionFactory
from src.offer.domain.ports import IOfferUnitOfWork, ITourUnitOfWork
from src.offer.infrastructure.storage.repository import (
    OfferRepository,
    TourRepository,
)


class OfferUnitOfWork(IOfferUnitOfWork):
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> None:
        self._session = self._session_factory.create_session()
        self.offer_repository = OfferRepository(self._session)

    def __exit__(self, *args) -> None:
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()


class TourUnitOfWork(ITourUnitOfWork):
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> None:
        self._session = self._session_factory.create_session()
        self.tour_repository = TourRepository(self._session)
        self.offer_repository = OfferRepository(self._session)

    def __exit__(self, *args) -> None:
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
