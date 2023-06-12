from typing import Any

import requests
from flask import Config
from requests.exceptions import ConnectionError

from src.consts import TripOfferApiEndpoints
from src.reservation.domain.exceptions import TripOfferServiceUnavailable
from src.reservation.domain.ports import (
    IEnrichReservationsWithOffersDataCommand,
)


class EnrichReservationsWithOffersDataCommand(
    IEnrichReservationsWithOffersDataCommand
):
    def __init__(self, config: Config) -> None:
        self._trip_offer_service_root_url = config.get(
            "TRIP_OFFER_SERVICE_ROOT_URL"
        )

    def __call__(
        self, reservations: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        offers_ids = [reservation["offer_id"] for reservation in reservations]
        try:
            offers_enrichment = requests.get(
                url=f"{self._trip_offer_service_root_url}"
                f"{TripOfferApiEndpoints.offers_enrichment}",
                json=dict(offers_ids=offers_ids),
            ).json()["offers_enrichment"]
        except ConnectionError:
            raise TripOfferServiceUnavailable

        return [
            reservation
            | {"offer_details": offers_enrichment[reservation["offer_id"]]}
            for reservation in reservations
        ]
