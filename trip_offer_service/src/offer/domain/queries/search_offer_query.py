from dataclasses import fields
from datetime import datetime

from src.consts import Collections
from src.offer.schema import SimpleOfferSchema
from src.infrastructure.storage import MongoReadOnlyClient
from src.offer.domain.ports import ISearchOfferQuery
from src.offer.infrastructure.queries.search import SearchOptions
from src.offer.infrastructure.storage.offer import SimpleOffer


class SearchOfferQuery(ISearchOfferQuery):
    def __init__(self, client: MongoReadOnlyClient) -> None:
        self.collection_name = Collections.offer_view
        self.client = client

    @staticmethod
    def _build_query(options: SearchOptions) -> dict:
        query = {}
        if options.city:
            query["city"] = options.city
        if options.country:
            query["country"] = options.country
        if options.operator:
            query["operator"] = options.operator
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
        if options.available:
            query["is_available"] = options.available
        return query

    @staticmethod
    def _build_projection() -> dict:
        projection = {field.name: 1 for field in fields(SimpleOffer)}
        projection["_id"] = 0
        return projection

    def count_offers(self, options: SearchOptions) -> int:
        query = self._build_query(options)
        return self.client.get_db()[self.collection_name].count_documents(query) 

    def search_offers(self, options: SearchOptions) -> list[SimpleOffer]:
        query = self._build_query(options)
        projection = self._build_projection()

        results = (
            self.client.get_db()[self.collection_name]
            .find(query, projection)
            .skip(options.page * options.page_size)
            .limit(options.page_size)
        )

        schema = SimpleOfferSchema()
        return schema.load(results, many=True)
