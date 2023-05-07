from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from uuid import UUID

if TYPE_CHECKING:
    from src.user.domain.dtos import UserDto


class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_gid(self, user_gid: UUID) -> Optional["UserDto"]:
        raise NotImplementedError


class IUserView(ABC):
    @abstractmethod
    def get_user_by_gid(self, user_gid: UUID) -> Optional["UserDto"]:
        raise NotImplementedError
