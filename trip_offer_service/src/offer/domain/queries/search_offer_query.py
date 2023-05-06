import re
from dataclasses import fields
from datetime import datetime
from typing import Any

from src.consts import Collections
from src.infrastructure.storage import MongoReadOnlyClient
from src.offer.domain.dtos import SearchOptions, SimpleOfferDto
from src.offer.domain.ports import ISearchOfferQuery
from src.offer.schema import SimpleOfferSchema


class SearchOfferQuery(ISearchOfferQuery):
    def __init__(self, client: MongoReadOnlyClient) -> None:
        self.collection_name = Collections.offer_view
        self.client = client

    @staticmethod
    def _ilike_condition(search_term: str) -> dict[str, re.Pattern]:
        regex = re.compile(search_term, re.IGNORECASE)
        return {"$regex": regex}

    def _build_query(self, options: SearchOptions) -> dict:
        query = {"is_available": True}

        if options.city:
            query["city"] = self._ilike_condition(options.city)
        if options.country:
            query["country"] = self._ilike_condition(options.country)
        if options.operator:
            query["operator"] = self._ilike_condition(options.operator)
        if options.date_start:
            query["departure_date"] = {
                "$gt": datetime.combine(options.date_start, datetime.min.time())
            }
        if options.date_end:
            query["arrival_date"] = {
                "$lt": datetime.combine(options.date_end, datetime.min.time())
            }
        if options.transport:
            query["transport"] = options.transport
        if options.adults:
            query["number_of_adults"] = {"$gte": options.adults}
        if options.kids:
            query["number_of_kids"] = {"$gte": options.kids}
        if options.room:
            query["room_type"] = options.room
        return query

    @staticmethod
    def _build_projection() -> dict:
        projection = {field.name: 1 for field in fields(SimpleOfferDto)}
        projection["_id"] = 0
        return projection

    def count_offers(self, options: SearchOptions) -> int:
        query = self._build_query(options)
        return self.client.get_db()[self.collection_name].count_documents(query)

    def search_offers(self, options: SearchOptions) -> list[SimpleOfferDto]:
        query = self._build_query(options)
        projection = self._build_projection()

        results = (
            self.client.get_db()[self.collection_name]
            .find(query, projection)
            .skip((options.page - 1) * options.page_size)
            .limit(options.page_size)
        )

        return SimpleOfferSchema().load(results, many=True)

    def get_search_options(self) -> dict[str, Any]:
        collection = self.client.get_db()[self.collection_name]
        fields = ["city", "country", "operator", "transport", "room_type"]

        return {field: collection.distinct(field) for field in fields}
