from http import HTTPStatus

import requests
from flask import Config, make_response
from webargs.flaskparser import use_args

from src.api import Resource
from src.api.blueprint import Blueprint
from src.api.error import custom_error
from src.consts import TripOfferApiEndpoints
from src.trip_offer.error import ERROR
from src.trip_offer.schema import TourSearchOptionsSchema


class SearchTourResource(Resource):
    def __init__(self, config: Config) -> None:
        self.trip_offer_service_root_url = config.get(
            "TRIP_OFFER_SERVICE_ROOT_URL"
        )

    @use_args(TourSearchOptionsSchema(), location="query")
    def get(self, options):
        try:
            response = requests.get(
                url=f"{self.trip_offer_service_root_url}{TripOfferApiEndpoints.tour_search}",
                params=options,
            )
        except ConnectionError:
            return custom_error(
                ERROR.trip_offer_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class SearchTourOptionsResource(Resource):
    def __init__(self, config: Config) -> None:
        self.trip_offer_service_root_url = config.get(
            "TRIP_OFFER_SERVICE_ROOT_URL"
        )

    def get(self):
        try:
            response = requests.get(
                url=f"{self.trip_offer_service_root_url}"
                f"{TripOfferApiEndpoints.tour_search_options}"
            )
        except ConnectionError:
            return custom_error(
                ERROR.trip_offer_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class Api(Blueprint):
    name = "tours"
    import_name = __name__

    resources = [
        (SearchTourResource, "/search"),
        (SearchTourOptionsResource, "/search/options"),
    ]
