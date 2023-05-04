from flask import Config
from injector import provider, singleton

from src.di_container.injector import Module
from src.infrastructure.message_broker import RabbitMQConnectionFactory
from src.infrastructure.storage import MongoClient, MongoReadOnlyClient

__all__ = ["InfrastructureModule"]


class InfrastructureModule(Module):
    @provider
    @singleton
    def provide_mongo_client(self, config: Config) -> MongoClient:
        return MongoClient(config)

    @provider
    @singleton
    def provide_mongo_readonly_client(
        self, config: Config
    ) -> MongoReadOnlyClient:
        return MongoReadOnlyClient(config)

    @provider
    @singleton
    def provide_rabbitmq_connection_factory(
        self, config: Config
    ) -> RabbitMQConnectionFactory:
        return RabbitMQConnectionFactory(config)
