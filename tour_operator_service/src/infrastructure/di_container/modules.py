from injector import Binder, provider, singleton

from src.config import Config
from src.di_container.injector import Module
from src.infrastructure.message_broker import RabbitMQConnectionFactory
from src.infrastructure.storage import SessionFactory, SQLAlchemyEngine


class InfrastructureModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(SessionFactory)

    @provider
    @singleton
    def provide_sqlalchemy_engine(self, config: Config) -> SQLAlchemyEngine:
        return SQLAlchemyEngine(config)

    @provider
    def provide_rabbitmq_connection_factory(
        self, config: Config
    ) -> RabbitMQConnectionFactory:
        return RabbitMQConnectionFactory(config)
