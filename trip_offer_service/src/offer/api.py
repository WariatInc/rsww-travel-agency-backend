from typing import Optional
from uuid import UUID
from math import ceil

from flask import jsonify, request
import marshmallow as ma

from src.api import Resource
from src.offer.schema import SearchOptionsSchema, OfferSchema, SimpleOfferSchema
from src.api.blueprint import Blueprint
from src.offer.domain.ports import IGetOfferQuery, ISearchOfferQuery
from src.offer.infrastructure.queries.search import SearchOptions
from src.offer.infrastructure.storage.offer import Offer, SimpleOffer


class OfferResource(Resource):
    def __init__(self, get_offer_query: IGetOfferQuery) -> None:
        self.get_offer_query = get_offer_query

    def get(self, uuid: UUID):
        schema = OfferSchema()
        offer: Optional[Offer] = self.get_offer_query.get_offer(uuid)
        if offer is None:
            return jsonify(
                ok=False,
                error=f"Invalid UUID: {uuid}"
            )

        return jsonify(
            ok=True,
            result=schema.dump(offer)
        )


class SearchOfferResource(Resource):
    def __init__(self, search_offer_query: ISearchOfferQuery) -> None:
        self.query = search_offer_query
    
    def get(self):
        try:
            schema = SearchOptionsSchema()
            options: SearchOptions = schema.load({
                name: val
                for (name, val) in request.args.items()
            }, unknown=ma.EXCLUDE)
        except ma.ValidationError as err:
            return jsonify(
                ok=False,
                error=f"Errors: {err.messages}"
            )
        number_of_offers = self.query.count_offers(options)
        offers: list[SimpleOffer] = self.query.search_offers(options)
        schema = SimpleOfferSchema(many=True)
        return jsonify(
            ok=True,
            max_page=ceil(number_of_offers / options.page_size),
            result=schema.dump(offers),
        )


class Api(Blueprint):
    name = "offer"
    import_name = __name__

    resources = [
        (OfferResource, "/get/<uuid:uuid>"),
        (SearchOfferResource, "/search/"),
    ]
