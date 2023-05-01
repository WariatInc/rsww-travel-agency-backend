from src.enum import StrEnum, auto


class Exchanges(StrEnum):
    reservation = auto()
    payment = auto()


class Queues(StrEnum):
    payment_service_reservation_queue = auto()
