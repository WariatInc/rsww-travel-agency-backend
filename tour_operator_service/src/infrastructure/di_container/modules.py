from injector import Binder, provider, singleton
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from src.config import Config
from src.di_container.injector import Module
from src.infrastructure.storage import SessionFactory, SQLAlchemyEngine


class InfrastructureModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(SessionFactory)

    @provider
    @singleton
    def provide_sqlalchemy_engine(self, config: Config) -> SQLAlchemyEngine:
        return SQLAlchemyEngine(config)

    @provider
    @singleton
    def provide_rabbitmq_connection(
        self, config: Config
    ) -> BlockingConnection:
        credentials = PlainCredentials(
            config.RABBITMQ_USER, config.RABBITMQ_PASSWORD
        )
        parameters = ConnectionParameters(
            host=config.RABBITMQ_HOST,
            port=config.RABBITMQ_PORT,
            credentials=credentials,
        )
        return BlockingConnection(parameters)
