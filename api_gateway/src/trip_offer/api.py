from http import HTTPStatus
from uuid import UUID

import requests
from flask import Config, make_response
from requests.exceptions import ConnectionError
from src.api import Resource
from src.api.blueprint import Blueprint
from src.api.error import custom_error
from src.consts import TripOfferApiEndpoints
from src.trip_offer.error import ERROR
from src.trip_offer.schema import OfferPriceGetSchema, SearchOfferSchema
from webargs.flaskparser import use_kwargs


class OfferResource(Resource):
    def __init__(self, config: Config) -> None:
        self.trip_offer_service_root_url = config.get(
            "TRIP_OFFER_SERVICE_ROOT_URL"
        )

    def get(self, offer_id: UUID):
        try:
            response = requests.get(
                url=f"{self.trip_offer_service_root_url}"
                f"{TripOfferApiEndpoints.get_offer.format(offer_id=str(offer_id))}",
            )
        except ConnectionError:
            return custom_error(
                ERROR.trip_offer_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class SearchOfferResource(Resource):
    def __init__(self, config: Config) -> None:
        self.trip_offer_service_root_url = config.get(
            "TRIP_OFFER_SERVICE_ROOT_URL"
        )

    @use_kwargs(SearchOfferSchema, location="query")
    def get(self, **search_params):
        try:
            response = requests.get(
                url=f"{self.trip_offer_service_root_url}"
                f"{TripOfferApiEndpoints.offer_search}",
                params=search_params,
            )
        except ConnectionError:
            return custom_error(
                ERROR.trip_offer_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class SearchOfferOptionsResource(Resource):
    def __init__(self, config: Config) -> None:
        self.trip_offer_service_root_url = config.get(
            "TRIP_OFFER_SERVICE_ROOT_URL"
        )

    def get(self):
        try:
            response = requests.get(
                url=f"{self.trip_offer_service_root_url}"
                f"{TripOfferApiEndpoints.offer_search_options}",
            )
        except ConnectionError:
            return custom_error(
                ERROR.trip_offer_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class OfferPriceResource(Resource):
    def __init__(self, config: Config) -> None:
        self.trip_offer_service_root_url = config.get(
            "TRIP_OFFER_SERVICE_ROOT_URL"
        )

    @use_kwargs(OfferPriceGetSchema, location="query")
    def get(self, offer_id: UUID, **kwargs):
        try:
            response = requests.get(
                url=f"{self.trip_offer_service_root_url}{TripOfferApiEndpoints.get_offer_price.format(offer_id=str(offer_id))}",
                params=kwargs,
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
        (OfferResource, "/<uuid:offer_id>"),
        (SearchOfferResource, "/search"),
        (SearchOfferOptionsResource, "/search/options"),
        (OfferPriceResource, "/price/<uuid:offer_id>"),
    ]
