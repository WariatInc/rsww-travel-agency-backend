from typing import TYPE_CHECKING, Any
import re
from dataclasses import fields

from src.infrastructure.storage import MongoReadOnlyClient
from src.consts import Collections
from src.offer.domain.dtos import OfferDto
from src.offer.schema import OfferSchema
from src.offers.domain.dtos import SearchOptions
from src.offers.domain.ports import IOffersView

if TYPE_CHECKING:
    from pymongo.collection import Collection


class OffersView(IOffersView):
    def __init__(self, mongo_client: MongoReadOnlyClient) -> None:
        self.collection: "Collection" = mongo_client.get_db()[Collections.offer]

    @staticmethod
    def _ilike_condition(search_term: str) -> dict[str, re.Pattern]:
        regex = re.compile(search_term, re.IGNORECASE)
        return {"$regex": regex}

    def _build_query(self, options: SearchOptions) -> dict:
        query: dict[str, Any] = {"tour_id": str(options.tour_id), "is_available": True}
        if options.room_type:
            query["room_type"] = self._ilike_condition(options.room_type)
        if options.all_inclusive:
            query["all_inclusive"] = options.all_inclusive
        if options.breakfast:
            query["breakfast"] = options.breakfast
        return query

    @staticmethod
    def _build_projection() -> dict:
        projection = {field.name: 1 for field in fields(OfferDto)}
        projection["_id"] = 0
        return projection

    def count(self, options: SearchOptions) -> int:
        query = self._build_query(options)
        return self.collection.count_documents(query)

    def search(self, options: SearchOptions) -> list[OfferDto]:
        query = self._build_query(options)
        projection = self._build_projection()

        results = (
            self.collection.find(query, projection)
            .skip((options.page - 1) * options.page_size)
            .limit(options.page_size)
        )

        offers = OfferSchema().load(results, many=True)
        return offers

    def search_options(self) -> dict[str, Any]:
        fields = ["room_type"]

        return {field: self.collection.distinct(field) for field in fields}
