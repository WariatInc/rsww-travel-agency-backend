from flask import Config
from injector import Binder, provider, singleton
from src.di_container.injector import Module
from src.infrastructure.storage import (ReadOnlySessionFactory, SessionFactory,
                                        SQLAlchemyEngine,
                                        SQLAlchemyReadOnlyEngine)

__all__ = ["InfrastructureModule"]


class InfrastructureModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(SessionFactory)
        self.bind(ReadOnlySessionFactory)

    @provider
    @singleton
    def provide_sqlalchemy_engine(self, config: Config) -> SQLAlchemyEngine:
        return SQLAlchemyEngine(config)

    @provider
    @singleton
    def provide_sqlalchemy_read_only_engine(
        self, config: Config
    ) -> SQLAlchemyReadOnlyEngine:
        return SQLAlchemyReadOnlyEngine(config)
