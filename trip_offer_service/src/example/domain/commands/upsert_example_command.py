from src.example.domain.ports import IExampleRepository, IUpsertExampleCommand
from src.example.infrastructure.storage.documents import Example


class UpsertExampleCommand(IUpsertExampleCommand):
    def __init__(self, example_repository: IExampleRepository) -> None:
        self.example_repository = example_repository

    def __call__(self, **kwargs) -> None:
        example = Example(**kwargs)
        self.example_repository.upsert(example)
