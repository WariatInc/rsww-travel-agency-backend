from typing import TYPE_CHECKING

from src.domain.dtos import ActorDto

if TYPE_CHECKING:
    from src.user.infrastructure.storage.models import User


def actor_dto_factory(user: "User") -> ActorDto:
    return ActorDto(
        gid=user.gid,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.last_name,
    )
