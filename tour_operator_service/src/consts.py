from src.enum import StrEnum, auto


class Exchanges(StrEnum):
    Offer = auto()
    Reservation = auto()


class Transport(StrEnum):
    self = auto()
    plane = auto()
    bus = auto()


class RoomType(StrEnum):
    standard = auto()
    family = auto()
    apartment = auto()
    studio = auto()


class ReservationState(StrEnum):
    accepted = auto()
    rejected = auto()


class RejectionReason(StrEnum):
    not_available = auto()
