from uuid import UUID
from dataclasses import fields
from datetime import datetime

from flask import Config

from src.offer.domain.ports import ISearchOfferQuery
from src.infrastructure.storage import MongoReadOnlyClient
from src.offer.infrastructure.storage.offer import SimpleOffer
from src.offer.infrastructure.queries.search import SearchOptions


class SearchOfferQuery(ISearchOfferQuery):
    def __init__(self,
                 config: Config,
                 client: MongoReadOnlyClient) -> None:
        self.collection_name = config["MONGO_VIEW_COLLECTION_NAME"]
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
                "$gt": datetime.fromisoformat(options.date_start)
            }
        if options.date_end:
            query["arrival_date"] = {
                "$lt": datetime.fromisoformat(options.date_end)
            }
        if options.transport:
            query["transport"] = options.transport
        if options.adults:
            query["number_of_adults"] = {
                "$gte": int(options.adults)
            }
        if options.kids:
            query["number_of_kids"] = {
                "$gte": int(options.kids)
            }
        if options.room:
            query["room_type"] = options.room
        if options.available:
            query["is_available"] = options.available
        return query
    
    @staticmethod
    def _build_projection() -> dict:
        projection = {
            field.name: 1
            for field in fields(SimpleOffer)
        }
        projection["_id"] = 0
        return projection 
    
    def search_offers(self, options: SearchOptions) -> list[SimpleOffer]:
        query = self._build_query(options)
        projection = self._build_projection()

        results = self.client.get_db()[self.collection_name].find(
            query, projection
        ).limit(options.max_offers)

        return [
            SimpleOffer.from_json(result)
            for result in results
        ]

