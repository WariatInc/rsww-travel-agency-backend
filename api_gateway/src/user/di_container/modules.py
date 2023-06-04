from injector import Binder

from src.di_container.injector import Module
from src.user.api import UserSessionResource
from src.user.domain.commands import (
    RevokeUserSessionCommand,
    UpdateUserSessionCommand,
)
from src.user.domain.ports import (
    IGetUserOnGivenPageCountQuery,
    IRevokeUserSessionCommand,
    IUpdateUserSessionCommand,
    IUserOnGivenPageCountView,
    IUserSessionUnitOfWork,
)
from src.user.domain.queries import GetUserOnGivenPageCountQuery
from src.user.infrastructure.storage.unit_of_work import UserSessionUnitOfWork
from src.user.infrastructure.storage.views import UserOnGivenPageCountView


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        # resources
        self.bind(UserSessionResource)

        # unit of works
        self.bind(IUserSessionUnitOfWork, UserSessionUnitOfWork)

        # views
        self.bind(IUserOnGivenPageCountView, UserOnGivenPageCountView)

        # commands
        self.bind(IRevokeUserSessionCommand, RevokeUserSessionCommand)
        self.bind(IUpdateUserSessionCommand, UpdateUserSessionCommand)

        # queries
        self.bind(IGetUserOnGivenPageCountQuery, GetUserOnGivenPageCountQuery)
