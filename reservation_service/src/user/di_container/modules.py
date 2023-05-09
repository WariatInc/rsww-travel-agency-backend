from injector import Binder
from src.di_container.injector import Module
from src.user.domain.ports import IUserView
from src.user.infrastructure.storage.views import UserView


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        # views
        self.bind(IUserView, UserView)
