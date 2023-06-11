from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.user.domain.dtos import UserSessionDto


class IUserSessionRepository(ABC):
    @abstractmethod
    def get_session(self, session_id: UUID) -> Optional[UserSessionDto]:
        raise NotImplementedError

    @abstractmethod
    def update_session(self, session_id: UUID, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_session(self, ip_address: str, webapp_page: str) -> UUID:
        raise NotImplementedError

    @abstractmethod
    def revoke_session(self, session_id: UUID) -> None:
        raise NotImplementedError


class IUserSessionUnitOfWork(ABC):
    user_session_repository: IUserSessionRepository

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class IUserOnGivenPageCountView(ABC):
    @abstractmethod
    def get(self, page: str) -> int:
        raise NotImplementedError


class IUpdateUserSessionCommand(ABC):
    @abstractmethod
    def __call__(
        self,
        ip_address: str,
        webapp_page: str,
        session_id: Optional[UUID] = None,
    ) -> UUID:
        raise NotImplementedError


class IRevokeUserSessionCommand(ABC):
    @abstractmethod
    def __call__(self, session_id: UUID) -> None:
        raise NotImplementedError


class IGetUserOnGivenPageCountQuery(ABC):
    @abstractmethod
    def get(self, page: str) -> int:
        raise NotImplementedError
