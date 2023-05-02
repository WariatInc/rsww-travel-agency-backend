from src.enum import StrEnum, auto


class ReservationState(StrEnum):
    pending = auto()
    rejected = auto()
    accepted = auto()
    cancelled = auto()
    paid = auto()


class Exchanges(StrEnum):
    reservation = auto()


class Queues(StrEnum):
    reservation_service_reservation_queue = auto()
    reservation_service_payment_queue = auto()
