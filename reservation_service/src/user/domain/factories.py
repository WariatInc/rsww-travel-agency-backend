from typing import TYPE_CHECKING

from src.user.domain.dtos import UserDto

if TYPE_CHECKING:
    from src.user.infrastructure.storage.models import User


def user_dto_factory(user: "User") -> UserDto:
    return UserDto(id=user.id, gid=user.gid)
