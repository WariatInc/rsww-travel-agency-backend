from http import HTTPStatus
from unittest import mock
from uuid import uuid4

import pytest

from src.example.api import ExampleResource, ExamplesResource
from src.example.domain.dtos import ExampleDto


class TestExampleResource:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.upsert_example_command_mock = mock.MagicMock()
        self.resource = ExampleResource(self.upsert_example_command_mock)

    def test_example_resource_post(self, app: pytest.fixture) -> None:
        uniq_id = uuid4()
        data = dict(author="test", title="test")

        with app.test_request_context(f"/api/examples/example/{uniq_id}", json=data):
            response = self.resource.post(uniq_id=uniq_id, **data)

            assert response[1] == HTTPStatus.CREATED
            assert response[0].json == {}

            self.upsert_example_command_mock.assert_called_once_with(
                uniq_id=uniq_id, **data
            )


class TestExamplesResource:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.get_example_list_query_mock = mock.MagicMock()
        self.resource = ExamplesResource(self.get_example_list_query_mock)

    def test_examples_resource_get(self, app: pytest.fixture) -> None:
        example_dto1 = ExampleDto(uniq_id=uuid4(), title="test1", author="test1")
        example_dto2 = ExampleDto(uniq_id=uuid4(), title="test2", author="test2")
        example_dto3 = ExampleDto(uniq_id=uuid4(), title="test3", author="test3")

        self.get_example_list_query_mock.return_value = [
            example_dto1,
            example_dto2,
            example_dto3,
        ]

        with app.test_request_context("/api/examples/"):
            response = self.resource.get()

            assert response[1] == HTTPStatus.OK
            assert response[0].json == [
                dict(
                    author=example_dto1.author,
                    title=example_dto1.title,
                    uniq_id=str(example_dto1.uniq_id),
                ),
                dict(
                    author=example_dto2.author,
                    title=example_dto2.title,
                    uniq_id=str(example_dto2.uniq_id),
                ),
                dict(
                    author=example_dto3.author,
                    title=example_dto3.title,
                    uniq_id=str(example_dto3.uniq_id),
                ),
            ]
