from src.enum import StrEnum, auto


class ReservationApiEndpoints(StrEnum):
    create_reservation = "/reservations"
    cancel_reservation = "/reservations/cancel/{reservation_id}"
    get_reservations = "/reservations?user_gid={user_gid}"
    delete_reservation = "/reservations/{reservation_id}?user_gid={user_gid}"
    get_reservation = "/reservations/{reservation_id}?user_gid={user_gid}"


class PaymentApiEndpoints(StrEnum):
    process_reservation_payment = "/payment/reservation"


class TripOfferApiEndpoints(StrEnum):
    get_offer = "/offers/{offer_id}"
    offer_search = "/offers/search"
    offer_search_options = "/offers/search/options"
    get_offer_price = "/offers/price/{offer_id}"


class TransportType(StrEnum):
    self = auto()
    bus = auto()
    plane = auto()


class RoomType(StrEnum):
    standard = auto()
    family = auto()
    apartment = auto()
    studio = auto()
