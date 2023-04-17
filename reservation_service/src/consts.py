from src.enum import StrEnum, auto


class ReservationState(StrEnum):
    PENDING = auto()
    REJECTED = auto()
    ACCEPTED = auto()
    CANCELLED = auto()
