from http import HTTPStatus
from uuid import UUID

import requests
from flask import Config, make_response
from webargs.flaskparser import use_args

from src.api.error import custom_error
from src.trip_offer.schema import OfferSearchOptionsSchema
from src.api.blueprint import Blueprint
from src.api import Resource
from src.consts import TripOfferApiEndpoints
from src.trip_offer.error import ERROR


class SearchOfferResource(Resource):
    def __init__(self, config: Config) -> None:
        self.trip_offer_service_root_url = config.get("TRIP_OFFER_SERVICE_ROOT_URL")

    @use_args(OfferSearchOptionsSchema(), location="query")
    def get(self, options):
        try:
            response = requests.get(
                url=f"{self.trip_offer_service_root_url}"
                f"{TripOfferApiEndpoints.offer_search}",
                params=options,
            )
        except ConnectionError:
            return custom_error(
                ERROR.trip_offer_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class SearchOfferOptionsResource(Resource):
    def __init__(self, config: Config) -> None:
        self.trip_offer_service_root_url = config.get("TRIP_OFFER_SERVICE_ROOT_URL")

    def get(self):
        try:
            response = requests.get(
                url=f"{self.trip_offer_service_root_url}"
                f"{TripOfferApiEndpoints.offer_search_options}"
            )
        except ConnectionError:
            return custom_error(
                ERROR.trip_offer_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class GetOfferResource(Resource):
    def __init__(self, config: Config) -> None:
        self.trip_offer_service_root_url = config.get("TRIP_OFFER_SERVICE_ROOT_URL")

    def get(self, id: UUID):
        try:
            response = requests.get(
                url=f"{self.trip_offer_service_root_url}"
                f"{TripOfferApiEndpoints.offer_view_get}".format(offer_id=str(id))
            )
        except ConnectionError:
            return custom_error(
                ERROR.trip_offer_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class Api(Blueprint):
    name = "offers"
    import_name = __name__

    resources = [
        (SearchOfferResource, "/search"),
        (SearchOfferOptionsResource, "/search/options"),
        (GetOfferResource, "/<uuid:id>"),
    ]
