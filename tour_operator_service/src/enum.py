import enum
from typing import Any, Reversible


def name_as_value(
    name: str, start: Any, count: int, last_values: Reversible
) -> Any:
    return name


class MetaStrEnum(enum.EnumMeta):
    def __contains__(cls, member: object) -> bool:
        if member is None:
            return False

        if isinstance(member, str):
            return member in cls.__members__.keys()

        return super().__contains__(member)


class StrEnum(str, enum.Enum, metaclass=MetaStrEnum):
    _generate_next_value_ = name_as_value

    def __str__(self) -> str:
        return self.value


auto = enum.auto
Enum = enum.Enum
IntEnum = enum.IntEnum
