from typing import TYPE_CHECKING

from src.domain.dtos import ActorDto

if TYPE_CHECKING:
    from src.user.infrastructure.storage.models import User


def actor_dto_factory(user: "User") -> ActorDto:
    return ActorDto(id=user.id, gid=user.gid)
