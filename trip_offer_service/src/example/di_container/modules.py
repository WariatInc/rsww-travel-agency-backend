from injector import Binder, provider, singleton
from pika import BlockingConnection

from src.di_container.injector import Module
from src.example.api import ExampleResource, ExamplesResource
from src.example.domain.commands import UpsertExampleCommand
from src.example.domain.ports import (
    IExampleRepository,
    IExamplesView,
    IGetExamplesListQuery,
    IUpsertExampleCommand,
)
from src.example.domain.queries import GetExamplesListQuery
from src.example.infrastructure.message_broker.publisher import (
    ExamplePublisher,
)
from src.example.infrastructure.storage.repository import ExampleRepository
from src.example.infrastructure.storage.views import ExamplesView


class ExampleModule(Module):
    def configure(self, binder: Binder) -> None:
        # resources
        self.bind(ExampleResource)
        self.bind(ExamplesResource)

        # repositories
        self.bind(IExampleRepository, ExampleRepository)

        # views
        self.bind(IExamplesView, ExamplesView)

        # commands
        self.bind(IUpsertExampleCommand, UpsertExampleCommand)

        # queries
        self.bind(IGetExamplesListQuery, GetExamplesListQuery)

    @provider
    @singleton
    def provide_example_publisher(
        self, connection: BlockingConnection
    ) -> ExamplePublisher:
        return ExamplePublisher(connection)
