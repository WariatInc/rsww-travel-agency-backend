from http import HTTPStatus
from math import ceil
from typing import Optional
from uuid import UUID

import marshmallow as ma
from flask import jsonify, request
from src.api import Resource
from src.api.blueprint import Blueprint
from src.api.error import custom_error, validation_error
from src.api.schema import use_schema
from src.offer.domain.dtos import OfferDto, SearchOptions, SimpleOfferDto
from src.offer.domain.exceptions import (InvalidOfferConfiguration,
                                         OfferNotFoundException)
from src.offer.domain.ports import (IGetOfferPriceQuery, IGetOfferQuery,
                                    ISearchOfferQuery)
from src.offer.error import ERROR
from src.offer.schema import (OfferPriceGetSchema, OfferPriceSchema,
                              OfferSchema, SearchOptionsSchema,
                              SimpleOfferSchema)
from webargs.flaskparser import use_kwargs


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


class OfferPriceResource(Resource):
    def __init__(self, get_offer_price: IGetOfferPriceQuery) -> None:
        self._get_offer_price = get_offer_price

    @use_kwargs(OfferPriceGetSchema, location="query")
    @use_schema(OfferPriceSchema, HTTPStatus.OK)
    def get(
        self, offer_id: UUID, kids_up_to_3: int = 0, kids_up_to_10: int = 0
    ):
        try:
            price = self._get_offer_price.get_price(
                offer_id, kids_up_to_3, kids_up_to_10
            )
        except OfferNotFoundException:
            return custom_error(
                ERROR.offer_not_found_error, HTTPStatus.NOT_FOUND
            )
        except InvalidOfferConfiguration:
            return custom_error(
                ERROR.invalid_offer_configuration_error, HTTPStatus.BAD_REQUEST
            )

        return {"price": price}


class Api(Blueprint):
    name = "offers"
    import_name = __name__

    resources = [
        (OfferResource, "/<uuid:offer_id>"),
        (SearchOfferResource, "/search"),
        (SearchOfferOptionsResource, "/search/options"),
        (OfferPriceResource, "/price/<uuid:offer_id>"),
    ]
