from src.infrastructure.storage import SessionFactory
from src.user.domain.ports import IUserSessionUnitOfWork
from src.user.infrastructure.storage.repository import UserSessionRepository


class UserSessionUnitOfWork(IUserSessionUnitOfWork):
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> None:
        self._session = self._session_factory.create_session()
        self.user_session_repository = UserSessionRepository(self._session)

    def __exit__(self, *args) -> None:
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
