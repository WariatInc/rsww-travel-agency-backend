import pytest

from src.example.domain.factories import example_dto_factory
from src.example.infrastructure.storage.views import ExamplesView


class TestExamplesView:
    @pytest.fixture(autouse=True)
    def setup(self, mongo_client: pytest.fixture) -> None:
        self.examples_view = ExamplesView(mongo_client)

    def test_get_list(self, db: pytest.fixture, example_factory) -> None:
        example1 = example_factory()
        example2 = example_factory()
        example3 = example_factory()

        examples = [example1, example2, example3]

        db.example.insert_many(examples)

        assert self.examples_view.get_list() == [
            example_dto_factory(e) for e in examples
        ]
