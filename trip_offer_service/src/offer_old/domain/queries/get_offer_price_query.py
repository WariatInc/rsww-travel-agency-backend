from math import ceil
from uuid import UUID

from src.consts import (
    AVERAGE_FLIGHT_COST_PER_COUNTRY,
    AVERAGE_NIGHT_COST_PER_COUNTRY,
    KIDS_FLIGHT_DISCOUNT,
    KIDS_HOTEL_DISCOUNT,
    PROVISION,
    ROOM_TYPE_MULTIPLIER,
    KidsAgeRange,
    TransportType,
)
from src.offer.domain.dtos import OfferDto
from src.offer.domain.exceptions import (
    InvalidOfferConfiguration,
    OfferNotFoundException,
)
from src.offer.domain.ports import IGetOfferPriceQuery, IGetOfferQuery


class GetOfferPriceQuery(IGetOfferPriceQuery):
    def __init__(self, get_offer_query: IGetOfferQuery) -> None:
        self._get_offer_query = get_offer_query

    @staticmethod
    def _calculate_hotel_price(
        offer: OfferDto,
        kids_up_to_18: int,
        kids_up_to_10: int,
        kids_up_to_3: int,
    ) -> float:
        hotel_cost = (
            AVERAGE_NIGHT_COST_PER_COUNTRY[offer.country]
            * ROOM_TYPE_MULTIPLIER[offer.room_type]
        ) * (offer.departure_date - offer.arrival_date).days

        return hotel_cost * (
            offer.number_of_adults
            + kids_up_to_18 * KIDS_HOTEL_DISCOUNT[KidsAgeRange.up_to_18]
            + kids_up_to_10 * KIDS_HOTEL_DISCOUNT[KidsAgeRange.up_to_10]
            + kids_up_to_3 * KIDS_HOTEL_DISCOUNT[KidsAgeRange.up_to_3]
        )

    @staticmethod
    def _calculate_flights_price(
        offer: OfferDto,
        kids_up_to_18: int,
        kids_up_to_10: int,
        kids_up_to_3: int,
    ):
        flight_cost = AVERAGE_FLIGHT_COST_PER_COUNTRY[offer.country]
        return (
            2
            * flight_cost
            * (
                offer.number_of_adults
                + kids_up_to_18 * KIDS_FLIGHT_DISCOUNT[KidsAgeRange.up_to_18]
                + kids_up_to_10 * KIDS_FLIGHT_DISCOUNT[KidsAgeRange.up_to_10]
                + kids_up_to_3 * KIDS_FLIGHT_DISCOUNT[KidsAgeRange.up_to_3]
            )
        )

    def get_price(
        self, offer_id: UUID, kids_up_to_3: int = 0, kids_up_to_10: int = 0
    ) -> float:
        offer = self._get_offer_query.get_offer(offer_id)

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
            if offer.transport == TransportType.plane
            else 0
        )

        return ceil((hotel_price + flight_price) * (1 + PROVISION)) - 0.01
