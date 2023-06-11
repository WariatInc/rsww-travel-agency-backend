from uuid import UUID

from src.consts import (
    KIDS_FLIGHT_DISCOUNT,
    KIDS_HOTEL_DISCOUNT,
    ROOM_TYPE_MULTIPLIER,
    KidsAgeRange,
    Transport,
)
from src.infrastructure.storage import ReadOnlySessionFactory
from src.offer.domain.exceptions import (
    InvalidOfferConfiguration,
    OfferNotFoundException,
)
from src.offer.domain.ports import IOfferPriceView
from src.offer.infrastructure.storage.models import Offer


class OfferPriceView(IOfferPriceView):
    def __init__(self, session_factory: ReadOnlySessionFactory) -> None:
        self._session = session_factory.create_session()

    @staticmethod
    def _calculate_extras_cost(offer: Offer) -> float:
        all_inclusive_cost_per_day = (
            0.15 * offer.tour.average_night_cost if offer.all_inclusive else 0
        )
        breakfast_cost_per_day = (
            0.05 * offer.tour.average_night_cost if offer.breakfast else 0
        )

        return all_inclusive_cost_per_day + breakfast_cost_per_day

    def _calculate_hotel_price(
        self,
        offer: Offer,
        kids_up_to_18: int,
        kids_up_to_10: int,
        kids_up_to_3: int,
    ) -> float:
        hotel_cost = (
            offer.tour.average_night_cost
            * ROOM_TYPE_MULTIPLIER[offer.room_type]
            + self._calculate_extras_cost(offer)
        ) * (offer.tour.departure_date - offer.tour.arrival_date).days

        return hotel_cost * (
            offer.number_of_adults
            + kids_up_to_18 * KIDS_HOTEL_DISCOUNT[KidsAgeRange.up_to_18]
            + kids_up_to_10 * KIDS_HOTEL_DISCOUNT[KidsAgeRange.up_to_10]
            + kids_up_to_3 * KIDS_HOTEL_DISCOUNT[KidsAgeRange.up_to_3]
        )

    @staticmethod
    def _calculate_flights_price(
        offer: Offer,
        kids_up_to_18: int,
        kids_up_to_10: int,
        kids_up_to_3: int,
    ) -> float:
        return (
            2
            * offer.tour.average_flight_cost
            * (
                offer.number_of_adults
                + kids_up_to_18 * KIDS_FLIGHT_DISCOUNT[KidsAgeRange.up_to_18]
                + kids_up_to_10 * KIDS_FLIGHT_DISCOUNT[KidsAgeRange.up_to_10]
                + kids_up_to_3 * KIDS_FLIGHT_DISCOUNT[KidsAgeRange.up_to_3]
            )
        )

    def get_offer_price(
        self, offer_id: UUID, kids_up_to_3: int, kids_up_to_10: int
    ) -> float:
        offer = (
            self._session.query(Offer)
            .filter(Offer.id == offer_id)
            .one_or_none()
        )

        if not offer:
            raise OfferNotFoundException

        if kids_up_to_3 + kids_up_to_10 > offer.number_of_kids:
            raise InvalidOfferConfiguration

        kids_up_to_18 = offer.number_of_kids - kids_up_to_3 - kids_up_to_10

        hotel_price = self._calculate_hotel_price(
            offer, kids_up_to_18, kids_up_to_10, kids_up_to_3
        )

        flight_price = (
            self._calculate_flights_price(
                offer, kids_up_to_18, kids_up_to_10, kids_up_to_3
            )
            if offer.tour.transport == Transport.plane
            else 0
        )

        return hotel_price + flight_price
