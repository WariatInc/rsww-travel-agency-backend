from abc import ABC, abstractmethod
from typing import Any

from src.example.domain.dtos import ExampleDto


class IExampleRepository(ABC):
    @abstractmethod
    def upsert(self, data: dict[str, Any]):
        raise NotImplementedError


class IUpsertExampleCommand(ABC):
    @abstractmethod
    def __call__(self, **kwargs) -> None:
        raise NotImplementedError


class IExamplesView(ABC):
    @abstractmethod
    def get_list(self) -> list[ExampleDto]:
        raise NotImplementedError


class IGetExamplesListQuery(ABC):
    @abstractmethod
    def __call__(self) -> list[ExampleDto]:
        raise NotImplementedError
