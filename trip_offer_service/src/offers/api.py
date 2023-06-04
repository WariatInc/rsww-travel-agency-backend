from http import HTTPStatus
from uuid import UUID
from math import ceil

from flask import jsonify
from webargs.flaskparser import use_args

from src.offers.domain.ports import (
    IQuerySearchOptions,
    IQueryCountOffers,
    IQuerySearchOffers,
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


class Api(Blueprint):
    name = "offers"
    import_name = __name__

    resources = [
        (SearchResource, "/search"),
        (SearchOptionsResource, "/search/options"),
    ]
