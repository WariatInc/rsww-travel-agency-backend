from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from src.consts import USER_SESSION_EXPIRE_IN
from src.user.domain.dtos import UserSessionDto
from src.user.domain.factories import user_session_dto_factory
from src.user.domain.ports import IUserSessionRepository
from src.user.infrastructure.storage.models import UserSession


class UserSessionRepository(IUserSessionRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_session_by_ip_address(
        self, ip_address: str
    ) -> Optional[UserSessionDto]:
        if (
            user_session := self._session.query(UserSession)
            .filter(UserSession.ip_address == ip_address, ~UserSession.revoked)
            .one_or_none()
        ):
            return user_session_dto_factory(user_session)

    def create_session(self, ip_address: str, webapp_page: str) -> None:
        user_session = UserSession(
            id=uuid4(),
            ip_address=ip_address,
            webapp_page=webapp_page,
            expires_in=USER_SESSION_EXPIRE_IN,
        )
        self._session.add(user_session)

    def revoke_session(self, session_id: UUID) -> None:
        self._session.query(UserSession).filter(
            UserSession.id == session_id
        ).update({UserSession.user_logout: True})

    def update_session(self, session_id: UUID, **kwargs) -> None:
        self._session.query(UserSession).filter(
            UserSession.id == session_id
        ).update(kwargs)
