from unittest import mock
from uuid import uuid4

import pytest

from src.example.domain.dtos import ExampleDto
from src.example.domain.queries import GetExamplesListQuery


class TestGetExampleListQuery:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.examples_view_mock = mock.MagicMock()
        self.get_example_list_query = GetExamplesListQuery(self.examples_view_mock)

    def test_get_example_list_query(self) -> None:
        example_dto1 = ExampleDto(uniq_id=uuid4(), title="test1", author="test1")
        example_dto2 = ExampleDto(uniq_id=uuid4(), title="test2", author="test2")
        example_dto3 = ExampleDto(uniq_id=uuid4(), title="test3", author="test3")

        self.examples_view_mock.get_list.return_value = [
            example_dto1,
            example_dto2,
            example_dto3,
        ]

        assert self.get_example_list_query() == [
            example_dto1,
            example_dto2,
            example_dto3,
        ]
        self.examples_view_mock.get_list.assert_called_once()
