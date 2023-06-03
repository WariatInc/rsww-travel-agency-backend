from src.enum import StrEnum, auto


class Exchanges(StrEnum):
    offer = auto()
    reservation = auto()


class Queues(StrEnum):
    tour_operator_reservation_queue = auto()


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
    invalid_offer_configuration = auto()
    offer_not_found = auto()


class KidsAgeRange(StrEnum):
    up_to_3 = auto()
    up_to_10 = auto()
    up_to_18 = auto()


ROOM_TYPE_MULTIPLIER = {
    RoomType.standard: 1,
    RoomType.family: 1.5,
    RoomType.studio: 0.75,
    RoomType.apartment: 2.5,
}


KIDS_HOTEL_DISCOUNT = {
    KidsAgeRange.up_to_3: 0.1,
    KidsAgeRange.up_to_10: 0.5,
    KidsAgeRange.up_to_18: 0.8,
}

KIDS_FLIGHT_DISCOUNT = {
    KidsAgeRange.up_to_3: 0.0,
    KidsAgeRange.up_to_10: 0.6,
    KidsAgeRange.up_to_18: 0.85,
}
