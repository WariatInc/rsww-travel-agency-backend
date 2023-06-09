import re
from dataclasses import fields
from typing import TYPE_CHECKING, Any
from uuid import UUID

import pymongo
from marshmallow import EXCLUDE

from src.consts import Collections, OfferSort, SortOrder
from src.infrastructure.storage import MongoReadOnlyClient
from src.offer.domain.dtos import OfferDto, OfferViewDto
from src.offer.schema import OfferSchema, OfferViewSchema
from src.offers.domain.dtos import SearchOptions
from src.offers.domain.factory import offer_view_dto_factory
from src.offers.domain.ports import IOffersView

if TYPE_CHECKING:
    from pymongo.collection import Collection


class OffersView(IOffersView):
    def __init__(self, mongo_client: MongoReadOnlyClient) -> None:
        self.offer_collection: "Collection" = mongo_client.get_db()[
            Collections.offer
        ]
        self.offer_view_collection: "Collection" = mongo_client.get_db()[
            Collections.offer_view
        ]

    @staticmethod
    def _ilike_condition(search_term: str) -> dict[str, re.Pattern]:
        regex = re.compile(search_term, re.IGNORECASE)
        return {"$regex": regex}

    @staticmethod
    def _build_offer_query(options: SearchOptions) -> dict:
        query: dict[str, Any] = {
            "tour_id": str(options.tour_id),
            "is_available": True,
        }
        if options.room_type:
            query["room_type"] = OffersView._ilike_condition(options.room_type)
        if options.all_inclusive:
            query["all_inclusive"] = options.all_inclusive
        if options.breakfast:
            query["breakfast"] = options.breakfast
        if options.adults is not None:
            query["number_of_adults"] = options.adults
        if options.kids is not None:
            query["number_of_kids"] = options.kids
        return query

    @staticmethod
    def _build_offer_projection() -> dict:
        projection = {field.name: 1 for field in fields(OfferDto)}
        projection["_id"] = 0
        return projection

    @staticmethod
    def _reorganize_offer_view(data: dict):
        try:
            result = data.copy()
            result["offer_id"] = result["id"]
            tour_data = result["tour"].copy()
            del result["id"]
            del result["tour"]
            result = dict(**result, **tour_data)
            return result
        except Exception as e:
            raise ValueError(f"Invalid offer_view data structure: {e}")

    def count(self, options: SearchOptions) -> int:
        query = self._build_offer_query(options)
        return self.offer_collection.count_documents(query)

    @staticmethod
    def _sort(
        query: pymongo.cursor.Cursor, sort_by: OfferSort, order: int
    ) -> pymongo.cursor.Cursor:
        if sort_by == OfferSort.price:
            return query.sort("price", order)
        return query

    def search(self, options: SearchOptions) -> list[OfferDto]:
        query = self._build_offer_query(options)
        projection = self._build_offer_projection()
        order = (
            pymongo.ASCENDING
            if options.sort_order == SortOrder.asc
            else pymongo.DESCENDING
        )

        results = self.offer_collection.find(query, projection)
        results = (
            self._sort(results, options.sort_by, order)
            .skip((options.page - 1) * options.page_size)
            .limit(options.page_size)
        )

        offers = OfferSchema().load(results, many=True)
        return offers

    def search_options(self) -> dict[str, Any]:
        fields = ["room_type"]

        return {
            field: self.offer_collection.distinct(field) for field in fields
        }

    def inspect(self, offer_id: UUID) -> OfferViewDto:
        query = {"id": str(offer_id)}
        results = list(self.offer_view_collection.find(query))
        schema = OfferViewSchema(unknown=EXCLUDE)

        if len(results) != 1:
            raise ValueError("Invalid Offer UUID")

        result = self._reorganize_offer_view(results[0])
        return schema.load(result)

    def get_offer_views_by_offer_ids(
        self, offers_ids: list[str]
    ) -> list[OfferViewDto]:
        offer_views = self.offer_view_collection.find(
            {"id": {"$in": offers_ids}}
        )
        return [
            offer_view_dto_factory(offer_view) for offer_view in offer_views
        ]

    def get_minimal_price_by_tour_ids(
        self, tour_ids: list[UUID]
    ) -> list[tuple[UUID, float]]:
        r = self.offer_collection.aggregate(
            [
                {"$match": {"tour_id": {"$in": [str(i) for i in tour_ids]}}},
                {
                    "$group": {
                        "_id": "$tour_id",
                        "min_price": {"$min": "$price"},
                    }
                },
            ]
        )
        return [(UUID(res["_id"]), float(res["min_price"])) for res in r]
