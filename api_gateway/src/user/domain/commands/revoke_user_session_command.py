from src.user.domain.ports import (
    IRevokeUserSessionCommand,
    IUserSessionUnitOfWork,
)


class RevokeUserSessionCommand(IRevokeUserSessionCommand):
    def __init__(self, uow: IUserSessionUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, ip_address: str) -> None:
        with self._uow:
            if user_session := self._uow.user_session_repository.get_session_by_ip_address(
                ip_address
            ):
                self._uow.user_session_repository.revoke_session(
                    user_session.id
                )
                self._uow.commit()
