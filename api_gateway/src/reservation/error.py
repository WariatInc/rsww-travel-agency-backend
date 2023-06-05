from src.enum import StrEnum, auto


class ERROR(StrEnum):
    reservation_service_unavailable = auto()
    trip_offer_service_unavailable = auto()
