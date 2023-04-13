from typing import TYPE_CHECKING

from src.example.domain.dtos import ExampleDto
from src.example.domain.factories import example_dto_factory
from src.example.domain.ports import IExamplesView
from src.example.infrastructure.storage.documents import Example
from src.infrastructure.storage import MongoReadOnlyClient

if TYPE_CHECKING:
    from pymongo.collection import Collection


class ExamplesView(IExamplesView):
    def __init__(self, mongo_client: MongoReadOnlyClient) -> None:
        self.collection: "Collection[Example]" = mongo_client.get_db().example

    def get_list(self) -> list[ExampleDto]:
        return [example_dto_factory(example) for example in self.collection.find()]
