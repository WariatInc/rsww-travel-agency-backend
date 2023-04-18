from flask import Config
from injector import provider, singleton
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from src.di_container.injector import Module
from src.infrastructure.storage import MongoClient, MongoReadOnlyClient

__all__ = ["InfrastructureModule"]


class InfrastructureModule(Module):
    @provider
    @singleton
    def provide_mongo_client(self, config: Config) -> MongoClient:
        return MongoClient(config)

    @provider
    @singleton
    def provide_mongo_readonly_client(self, config: Config) -> MongoReadOnlyClient:
        return MongoReadOnlyClient(config)

    @provider
    @singleton
    def provide_rabbitmq_connection(self, config: Config) -> BlockingConnection:
        credentials = PlainCredentials(
            config.get("RABBITMQ_USER"), config.get("RABBITMQ_PASSWORD")
        )
        parameters = ConnectionParameters(
            host=config.get("RABBITMQ_HOST"),
            port=config.get("RABBITMQ_PORT"),
            credentials=credentials,
        )
        return BlockingConnection(parameters)
