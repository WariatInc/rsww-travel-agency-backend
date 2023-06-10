from src.enum import IntEnum, StrEnum, auto


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


class CancelReason(StrEnum):
    payment_timeout = auto()
    cancelled_by_user = auto()


PROVISION = 0.1

ACCEPTED_RESERVATION_TIMEOUT = 120


class TimeSeconds(IntEnum):
    minute = 60
    hour = 3600


TIME_TO_SEE_CANCELLED_OR_REJECTED_RESERVATIONS = TimeSeconds.minute * 5
