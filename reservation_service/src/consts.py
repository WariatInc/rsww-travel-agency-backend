from src.enum import StrEnum, auto


class ReservationState(StrEnum):
    pending = auto()
    rejected = auto()
    accepted = auto()
    cancelled = auto()


class Exchanges(StrEnum):
    reservation = auto()


class Queues(StrEnum):
    reservation_service_reservation_queue = auto()
