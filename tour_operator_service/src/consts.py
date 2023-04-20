from src.enum import StrEnum, auto


class Exchanges(StrEnum):
    Offer = auto()


class Transport(StrEnum):
    self = auto()
    plane = auto()
    bus = auto()


class RoomType(StrEnum):
    standard = auto()
    family = auto()
    apartment = auto()
    studio = auto()
