from src.enum import StrEnum, auto


class Exchanges(StrEnum):
    reservation = auto()
    payment = auto()


class Queues(StrEnum):
    payment_service_reservation_queue = auto()


class ReservationState(StrEnum):
    accepted = auto()
    rejected = auto()
    pending = auto()
    cancelled = auto()
    paid = auto()


class PaymentItem(StrEnum):
    reservation = auto()


class PaymentState(StrEnum):
    finalized = auto()
    rejected = auto()
    pending = auto()


RESERVATION_READ_STORE_COLUMNS = ["reservation_id", "state", "price"]
