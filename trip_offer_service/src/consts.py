from enum import Enum, auto
from typing import Any


class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> Any:
        return name


class EXCHANGES(AutoName):
    example = auto()


class Collections:
    offer_view = "offer_view"
