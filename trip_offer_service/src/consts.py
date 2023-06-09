from src.enum import StrEnum, auto


class Exchanges(StrEnum):
    example = auto()
    offer = auto()


class Queues(StrEnum):
    trip_offer_service_offer_queue = auto()


class Collections(StrEnum):
    tour = "Tour"
    offer = "Offer"
    offer_view = "OfferView"


class TransportType(StrEnum):
    self = auto()
    bus = auto()
    plane = auto()


class RoomType(StrEnum):
    standard = auto()
    family = auto()
    apartment = auto()
    studio = auto()
