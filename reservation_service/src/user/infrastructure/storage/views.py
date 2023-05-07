from typing import TYPE_CHECKING, Optional
from uuid import UUID

from src.infrastructure.storage import ReadOnlySessionFactory
from src.user.domain.factories import user_dto_factory
from src.user.domain.ports import IUserView
from src.user.infrastructure.storage.models import User

if TYPE_CHECKING:
    from src.user.domain.dtos import UserDto


class UserView(IUserView):
    def __init__(self, session_factory: ReadOnlySessionFactory) -> None:
        self._session = session_factory.create_session()

    def get_user_by_gid(self, user_gid: UUID) -> Optional["UserDto"]:
        if (
            user := self._session.query(User)
            .filter(User.gid == user_gid)
            .one_or_none()
        ):
            return user_dto_factory(user)
