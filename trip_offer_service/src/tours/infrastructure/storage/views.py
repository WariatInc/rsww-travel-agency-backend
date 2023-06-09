import re
from dataclasses import fields
from datetime import datetime
from typing import TYPE_CHECKING, Any

from src.consts import Collections
from src.infrastructure.storage import MongoReadOnlyClient
from src.tour.domain.dtos import TourDto
from src.tour.schema import TourSchema
from src.tours.domain.dtos import SearchOptions
from src.tours.domain.ports import IToursView
from src.offers.domain.ports import IOffersView

if TYPE_CHECKING:
    from pymongo.collection import Collection


class ToursView(IToursView):
    def __init__(
        self, mongo_client: MongoReadOnlyClient, offers: IOffersView
    ) -> None:
        self.collection: "Collection" = mongo_client.get_db()[Collections.tour]
        self.offers = offers

    @staticmethod
    def _ilike_condition(search_term: str) -> dict[str, re.Pattern]:
        regex = re.compile(search_term, re.IGNORECASE)
        return {"$regex": regex}

    def _build_query(self, options: SearchOptions) -> dict:
        query: dict[str, Any] = {}

        if options.departure_city:
            query["departure_city"] = self._ilike_condition(
                options.departure_city
            )
        if options.country:
            query["country"] = self._ilike_condition(options.country)
        if options.operator:
            query["operator"] = self._ilike_condition(options.operator)
        if options.date_start:
            query["departure_date"] = {
                "$gt": datetime.combine(
                    options.date_start, datetime.min.time()
                )
            }
        if options.date_end:
            query["arrival_date"] = {
                "$lt": datetime.combine(options.date_end, datetime.min.time())
            }
        if options.transport:
            query["transport"] = options.transport
        return query

    @staticmethod
    def _build_projection() -> dict:
        projection = {field.name: 1 for field in fields(TourDto)}
        projection["_id"] = 0
        return projection

    def count(self, options: SearchOptions) -> int:
        query = self._build_query(options)
        return self.collection.count_documents(query)

    def search(self, options: SearchOptions) -> list[TourDto]:
        query = self._build_query(options)
        projection = self._build_projection()

        results = (
            self.collection.find(query, projection)
            .skip((options.page - 1) * options.page_size)
            .limit(options.page_size)
        )

        tours: list[TourDto] = TourSchema().load(results, many=True)

        tours_by_uuid = {tour.id: tour for tour in tours}
        for uuid, price in self.offers.get_minimal_price_by_tour_ids(
            list(tours_by_uuid.keys())
        ):
            tours_by_uuid[uuid].lowest_price = price

        return tours

    def search_options(self) -> dict[str, Any]:
        fields = ["city", "country", "operator", "transport", "room_type"]

        return {field: self.collection.distinct(field) for field in fields}
