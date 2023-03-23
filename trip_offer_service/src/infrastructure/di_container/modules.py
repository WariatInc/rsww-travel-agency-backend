from flask import Config
from injector import Binder, provider, singleton

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
    def provide_mongo_readonly_client(
        self, config: Config
    ) -> MongoReadOnlyClient:
        return MongoReadOnlyClient(config)
