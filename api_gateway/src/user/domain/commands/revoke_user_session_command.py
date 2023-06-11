from uuid import UUID

from src.user.domain.ports import (
    IRevokeUserSessionCommand,
    IUserSessionUnitOfWork,
)


class RevokeUserSessionCommand(IRevokeUserSessionCommand):
    def __init__(self, uow: IUserSessionUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, session_id: UUID) -> None:
        with self._uow:
            if user_session := self._uow.user_session_repository.get_session(
                session_id
            ):
                self._uow.user_session_repository.revoke_session(
                    user_session.id
                )
                self._uow.commit()
