from typing import TYPE_CHECKING

from src.user.domain.dtos import UserSessionDto

if TYPE_CHECKING:
    from src.user.infrastructure.storage.models import UserSession


def user_session_dto_factory(user_session: "UserSession") -> UserSessionDto:
    return UserSessionDto(
        id=user_session.id,
        ip_address=user_session.ip_address,
        webapp_page=user_session.webapp_page,
        expires_in=user_session.expires_in,
        refreshed_at=user_session.refreshed_at,
        revoked=user_session.revoked,
    )
