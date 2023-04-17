from flask import Config
from injector import Binder, provider, singleton
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from src.di_container.injector import Module
from src.infrastructure.storage import (
    ReadOnlySessionFactory,
    SessionFactory,
    SQLAlchemyEngine,
    SQLAlchemyReadOnlyEngine,
)

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

    @provider
    @singleton
    def provide_rabbitmq_connection(
        self, config: Config
    ) -> BlockingConnection:
        credentials = PlainCredentials(
            config.get("RABBITMQ_USER"), config.get("RABBITMQ_PASSWORD")
        )
        parameters = ConnectionParameters(
            host=config.get("RABBITMQ_HOST"),
            port=config.get("RABBITMQ_PORT"),
            credentials=credentials,
        )
        return BlockingConnection(parameters)
