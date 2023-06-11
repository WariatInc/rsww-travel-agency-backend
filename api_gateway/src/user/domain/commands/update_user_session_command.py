from typing import Optional
from uuid import UUID

from src.user.domain.ports import (
    IUpdateUserSessionCommand,
    IUserSessionUnitOfWork,
)
from src.utils import get_current_time


class UpdateUserSessionCommand(IUpdateUserSessionCommand):
    def __init__(self, uow: IUserSessionUnitOfWork) -> None:
        self._uow = uow

    def __call__(
        self,
        ip_address: str,
        webapp_page: str,
        session_id: Optional[UUID] = None,
    ) -> UUID:
        with self._uow:
            if session_id and self._uow.user_session_repository.get_session(
                session_id
            ):
                self._uow.user_session_repository.update_session(
                    session_id,
                    webapp_page=webapp_page,
                    refreshed_at=get_current_time(),
                )
                self._uow.commit()
                return session_id

            new_session_id = self._uow.user_session_repository.create_session(
                ip_address=ip_address, webapp_page=webapp_page
            )
            self._uow.commit()
            return new_session_id
