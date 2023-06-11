from src.infrastructure.storage import ReadOnlySessionFactory
from src.user.domain.ports import IUserOnGivenPageCountView
from src.user.infrastructure.storage.models import UserSession


class UserOnGivenPageCountView(IUserOnGivenPageCountView):
    def __init__(self, session_factory: ReadOnlySessionFactory) -> None:
        self._session = session_factory.create_session()

    def get(self, page: str) -> int:
        return (
            self._session.query(UserSession)
            .filter(UserSession.webapp_page == page, ~UserSession.revoked)
            .count()
        )
