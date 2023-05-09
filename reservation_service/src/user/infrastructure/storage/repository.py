from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.user.domain.factories import user_dto_factory
from src.user.domain.ports import IUserRepository
from src.user.infrastructure.storage.models import User

if TYPE_CHECKING:
    from src.user.domain.dtos import UserDto


class UserRepository(IUserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_user_by_gid(self, user_gid: UUID) -> Optional["UserDto"]:
        if (
            user := self._session.query(User)
            .filter(User.gid == user_gid)
            .one_or_none()
        ):
            return user_dto_factory(user)
