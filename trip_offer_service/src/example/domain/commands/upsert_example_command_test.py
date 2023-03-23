from unittest import mock
from uuid import uuid4

import pytest

from src.example.domain.commands import UpsertExampleCommand


class TestUpsertExampleCommand:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.example_repository_mock = mock.MagicMock()
        self.upsert_example_command = UpsertExampleCommand(
            self.example_repository_mock
        )

    def test_upsert_command(self) -> None:
        data = dict(uniq_id=uuid4(), title="test", author="test")
        self.upsert_example_command(**data)

        self.example_repository_mock.upsert.assert_called_once_with(data)
