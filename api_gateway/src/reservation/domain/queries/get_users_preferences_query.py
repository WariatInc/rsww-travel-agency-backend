from collections import Counter

import requests
from flask import Config

from src.consts import USER_PREFERENCES_LIST_LENGTH, TripOfferApiEndpoints
from src.reservation.domain.exceptions import TripOfferServiceUnavailable
from src.reservation.domain.ports import IGetUsersPreferencesQuery


class GetUsersPreferencesQuery(IGetUsersPreferencesQuery):
    def __init__(self, config: Config) -> None:
        self._trip_offer_service_root_url = config.get(
            "TRIP_OFFER_SERVICE_ROOT_URL"
        )

    def get(self, offers_ids: list[str]) -> dict[str, str]:
        try:
            offers_details = requests.get(
                url=f"{self._trip_offer_service_root_url}"
                f"{TripOfferApiEndpoints.offers_enrichment}",
                json=dict(offers_ids=offers_ids),
            ).json()["offers_enrichment"]
        except ConnectionError:
            raise TripOfferServiceUnavailable

        if not offers_details:
            return {}

        hotels = [offer.get("hotel") for offer in offers_details.values()]
        room_types = [
            offer.get("room_type") for offer in offers_details.values()
        ]
        countries = [offer.get("country") for offer in offers_details.values()]

        return {
            "hotels": [
                hotel
                for hotel, no_offers in Counter(hotels).most_common(
                    USER_PREFERENCES_LIST_LENGTH
                )
            ],
            "room_types": [
                room_type
                for room_type, no_offers in Counter(room_types).most_common(
                    USER_PREFERENCES_LIST_LENGTH
                )
            ],
            "countries": [
                country
                for country, no_offers in Counter(countries).most_common(
                    USER_PREFERENCES_LIST_LENGTH
                )
            ],
        }
