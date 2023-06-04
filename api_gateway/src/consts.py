from src.enum import StrEnum, auto


class ReservationApiEndpoints(StrEnum):
    create_reservation = "/reservations"
    cancel_reservation = "/reservations/cancel/{reservation_id}"
    get_reservations = "/reservations?user_gid={user_gid}"
    delete_reservation = "/reservations/{reservation_id}?user_gid={user_gid}"
    get_reservation = "/reservations/{reservation_id}?user_gid={user_gid}"
    get_reservation_events_dashboard = "/reservations/events"


class PaymentApiEndpoints(StrEnum):
    process_reservation_payment = "/payment/reservation"


class TripOfferApiEndpoints(StrEnum):
    tour_search = "/tours/search"
    tour_search_options = "/tours/search/options"
    offer_search = "/offers/search"
    offer_search_options = "/offers/search/options"
    offer_view_get = "/offers/{offer_id}"


class TransportType(StrEnum):
    self = auto()
    bus = auto()
    plane = auto()


class RoomType(StrEnum):
    standard = auto()
    family = auto()
    apartment = auto()
    studio = auto()


USER_SESSION_EXPIRE_IN = 300
