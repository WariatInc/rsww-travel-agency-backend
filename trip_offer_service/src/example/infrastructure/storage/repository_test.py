from uuid import uuid4

import pytest
from src.example.infrastructure.storage.repository import ExampleRepository


class TestExampleRepository:
    @pytest.fixture(autouse=True)
    def setup(self, mongo_client: pytest.fixture) -> None:
        self.example_repository = ExampleRepository(mongo_client)

    def test_insert_upsert(self, db: pytest.fixture, example_factory) -> None:
        example1 = example_factory()
        db.example.insert_one(example1)

        uniq_id = uuid4()
        data = dict(uniq_id=uniq_id, author="test", title="test")

        self.example_repository.upsert(data)
        result = db.example.find_one({"uniq_id": uniq_id})

        assert data == dict(
            uniq_id=result.get("uniq_id"),
            title=result.get("title"),
            author=result.get("author"),
        )
        assert db.example.count_documents({}) == 2

    def test_update_upsert(self, db: pytest.fixture, example_factory) -> None:
        uniq_id = uuid4()
        example1 = example_factory(uniq_id=uniq_id)
        example2 = example_factory()
        db.example.insert_many([example1, example2])

        data = dict(uniq_id=uniq_id, author="changed", title="changed")
        self.example_repository.upsert(data)

        result = db.example.find_one({"uniq_id": uniq_id})

        assert data == dict(
            uniq_id=result.get("uniq_id"),
            title=result.get("title"),
            author=result.get("author"),
        )
        assert db.example.count_documents({}) == 2
