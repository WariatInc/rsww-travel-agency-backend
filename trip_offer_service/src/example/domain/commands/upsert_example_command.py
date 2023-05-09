from src.domain.events import event_factory
from src.example.domain.events import ExampleUpdatedEvent
from src.example.domain.ports import IExampleRepository, IUpsertExampleCommand
from src.example.infrastructure.message_broker.publisher import \
    ExamplePublisher
from src.example.infrastructure.storage.documents import Example


class UpsertExampleCommand(IUpsertExampleCommand):
    def __init__(
        self,
        example_repository: IExampleRepository,
        publisher: ExamplePublisher,
    ) -> None:
        self.example_repository = example_repository
        self.publisher = publisher

    def __call__(self, **kwargs) -> None:
        example = Example(**kwargs)
        self.example_repository.upsert(example)

        example_id = kwargs.pop("uniq_id")
        event = event_factory(
            ExampleUpdatedEvent, example_id=example_id, details=kwargs
        )

        self.publisher.publish(event)
