from http import HTTPStatus
from math import ceil
from typing import Optional
from uuid import UUID

import marshmallow as ma
from flask import jsonify, request

from src.api import Resource
from src.api.blueprint import Blueprint
from src.api.error import custom_error, validation_error
from src.offer.domain.dtos import OfferDto, SearchOptions, SimpleOfferDto
from src.offer.domain.ports import IGetOfferQuery, ISearchOfferQuery
from src.offer.schema import (
    OfferSchema,
    SearchOptionsSchema,
    SimpleOfferSchema,
)


class OfferResource(Resource):
    def __init__(self, get_offer_query: IGetOfferQuery) -> None:
        self.get_offer_query = get_offer_query

    def get(self, offer_id: UUID):
        offer: Optional[OfferDto] = self.get_offer_query.get_offer(offer_id)
        if not offer:
            return custom_error(
                f"Provided UUID={offer_id} could not be found.",
                HTTPStatus.NOT_FOUND,
            )

        return jsonify(OfferSchema().dump(offer))


class SearchOfferResource(Resource):
    def __init__(self, search_offer_query: ISearchOfferQuery) -> None:
        self.query = search_offer_query

    def get(self):
        try:
            options: SearchOptions = SearchOptionsSchema().load(
                request.args,
                unknown=ma.EXCLUDE,
            )
        except ma.ValidationError as err:
            return validation_error(err.messages)

        number_of_offers = self.query.count_offers(options)
        offers: list[SimpleOfferDto] = self.query.search_offers(options)
        return jsonify(
            max_page=ceil(number_of_offers / options.page_size),
            result=SimpleOfferSchema(many=True).dump(offers),
        )


class SearchOfferOptionsResource(Resource):
    def __init__(self, search_offer_query: ISearchOfferQuery) -> None:
        self.query = search_offer_query

    def get(self):
        return jsonify(self.query.get_search_options())


class Api(Blueprint):
    name = "offers"
    import_name = __name__

    resources = [
        (OfferResource, "/<uuid:offer_id>"),
        (SearchOfferResource, "/search"),
        (SearchOfferOptionsResource, "/search/options"),
    ]
