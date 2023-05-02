from uuid import UUID
import dataclasses

from flask import jsonify, request

from src.api import Resource
from src.api.blueprint import Blueprint
from src.offer.infrastructure.storage.offer import Offer, SimpleOffer
from src.offer.infrastructure.queries.search import SearchOptions
from src.offer.domain.ports import (
    IGetOfferQuery,
    ISearchOfferQuery
)


class OfferResource(Resource):
    def __init__(self, get_offer_query: IGetOfferQuery) -> None:
        self.get_offer_query = get_offer_query

    def get(self, uuid: UUID):
        offer: Offer = self.get_offer_query.get_offer(
            uuid
        )
        return jsonify(
            **offer.to_json()
        )


class SearchOfferResource(Resource):
    def __init__(self, search_offer_query: ISearchOfferQuery) -> None:
        self.query = search_offer_query

    def get(self):
        possible_options = {
            field.name
            for field in dataclasses.fields(SearchOptions)
        }
        options = SearchOptions()
        for option_name, option_val in request.args.items():
            if option_name not in possible_options:
                return jsonify(
                    ok=False,
                    error=f"Invalid option: {option_name}"
                )
            setattr(options, option_name, option_val)

        offers: list[SimpleOffer] = self.query.search_offers(options)
        return jsonify(
            result=[
                offer.to_json()
                for offer in offers
            ],
            ok=True,
        )


class Api(Blueprint):
    name = "offer"
    import_name = __name__

    resources = [
        (OfferResource, "/get/<uuid:uuid>"),
        (SearchOfferResource, "/search/"),
    ]
