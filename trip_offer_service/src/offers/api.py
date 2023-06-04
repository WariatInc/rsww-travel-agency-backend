from http import HTTPStatus
from uuid import UUID
from math import ceil

from flask import jsonify
from webargs.flaskparser import use_args
import marshmallow as ma

from src.api.error import custom_error, validation_error
from src.offers.domain.ports import (
    IQuerySearchOptions,
    IQueryCountOffers,
    IQuerySearchOffers,
    IQueryOffer,
)
from src.offers.schema import SearchOptionsSchema
from src.offer.schema import OfferSchema
from src.offers.domain.dtos import SearchOptions
from src.api.blueprint import Blueprint
from src.api import Resource


class SearchResource(Resource):
    def __init__(
        self, search: IQuerySearchOffers, count_offers: IQueryCountOffers
    ) -> None:
        self.search = search
        self.count_offers = count_offers

    @use_args(SearchOptionsSchema(), location="query")
    def get(self, options: SearchOptions):
        offer_schema = OfferSchema(many=True)
        offers = offer_schema.dump(self.search(options))
        number_of_offers = self.count_offers(options)
        return jsonify(
            max_page=ceil(number_of_offers / options.page_size),
            result=offers,
        )


class SearchOptionsResource(Resource):
    def __init__(self, get_search_options: IQuerySearchOptions) -> None:
        self.get_search_options = get_search_options

    def get(self):
        return jsonify(self.get_search_options())


class OfferViewResource(Resource):
    def __init__(self, get_offer: IQueryOffer) -> None:
        self.get_offer = get_offer

    def get(self, offer_id: UUID):
        try:
            return jsonify(self.get_offer(offer_id))
        except ValueError as err:
            return custom_error(str(err), HTTPStatus.NOT_FOUND)
        except ma.ValidationError as err:
            return validation_error(err.messages)


class Api(Blueprint):
    name = "offers"
    import_name = __name__

    resources = [
        (OfferViewResource, "/<uuid:offer_id>"),
        (SearchResource, "/search"),
        (SearchOptionsResource, "/search/options"),
    ]
