from src.user.domain.ports import (
    IUpdateUserSessionCommand,
    IUserSessionUnitOfWork,
)
from src.utils import get_current_time


class UpdateUserSessionCommand(IUpdateUserSessionCommand):
    def __init__(self, uow: IUserSessionUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, ip_address: str, webapp_page: str) -> None:
        with self._uow:
            if user_session := self._uow.user_session_repository.get_session_by_ip_address(
                ip_address
            ):
                self._uow.user_session_repository.update_session(
                    user_session.id,
                    webapp_page=webapp_page,
                    refreshed_at=get_current_time(),
                )
            else:
                self._uow.user_session_repository.create_session(
                    ip_address=ip_address, webapp_page=webapp_page
                )

            self._uow.commit()
