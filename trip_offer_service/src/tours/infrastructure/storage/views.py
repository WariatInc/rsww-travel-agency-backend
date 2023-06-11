import re
from dataclasses import fields
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID

import pymongo

from src.consts import Collections, SortOrder, TourSort
from src.infrastructure.storage import MongoReadOnlyClient
from src.offers.domain.ports import IOffersView
from src.tours.domain.dtos import SearchOptions, TourDto
from src.tours.domain.factory import tour_dto_factory
from src.tours.domain.ports import IToursView, ITourView

if TYPE_CHECKING:
    from pymongo.collection import Collection


class ToursView(IToursView):
    def __init__(
        self, mongo_client: MongoReadOnlyClient, offers: IOffersView
    ) -> None:
        self.tour_collection: "Collection" = mongo_client.get_db()[
            Collections.tour
        ]
        self.offer_collection: "Collection" = mongo_client.get_db()[
            Collections.offer
        ]
        self.offers = offers

    @staticmethod
    def _ilike_condition(search_term: str) -> dict[str, re.Pattern]:
        regex = re.compile(search_term, re.IGNORECASE)
        return {"$regex": regex}

    def _build_query(self, options: SearchOptions) -> dict:
        query: dict[str, Any] = {}

        if options.departure_city:
            query["tour.departure_city"] = self._ilike_condition(
                options.departure_city
            )
        if options.country:
            query["tour.country"] = self._ilike_condition(options.country)
        if options.operator:
            query["tour.operator"] = self._ilike_condition(options.operator)
        if options.date_start:
            query["tour.departure_date"] = {
                "$gt": datetime.combine(
                    options.date_start, datetime.min.time()
                )
            }
        if options.date_end:
            query["tour.arrival_date"] = {
                "$lt": datetime.combine(options.date_end, datetime.min.time())
            }
        if options.transport:
            query["tour.transport"] = options.transport

        if options.kids:
            query["number_of_kids"] = options.kids

        if options.adults:
            query["number_of_adults"] = options.adults

        return query

    @staticmethod
    def _build_projection() -> dict:
        projection = {f"tour.{field.name}": 1 for field in fields(TourDto)}
        projection["_id"] = 0
        projection["min_price"] = 1
        return projection

    @staticmethod
    def _sort(sort_by: TourSort, order: int) -> dict:
        if sort_by == TourSort.arrival_date:
            return {"tour.departure_date": order}
        if sort_by == TourSort.price:
            return {"min_price": order}
        return {}

    def _build_pipeline(self, options) -> list[dict]:
        order = (
            pymongo.ASCENDING
            if options.sort_order == SortOrder.asc
            else pymongo.DESCENDING
        )
        return [
            {
                "$lookup": {
                    "from": Collections.tour,
                    "localField": "tour_id",
                    "foreignField": "id",
                    "as": "tour",
                }
            },
            {"$match": self._build_query(options)},
            {
                "$group": {
                    "_id": "$tour_id",
                    "tour": {"$first": "$tour"},
                    "min_price": {"$min": "$price"},
                }
            },
            {"$project": self._build_projection()},
            {"$sort": self._sort(options.sort_by, order)},
            {
                "$facet": {
                    "tours": [
                        {"$skip": (options.page - 1) * options.page_size},
                        {"$limit": options.page_size},
                    ],
                    "count": [{"$count": "total_results"}],
                }
            },
        ]

    def search(self, options: SearchOptions) -> tuple[list[TourDto], int]:
        results = list(
            self.offer_collection.aggregate(self._build_pipeline(options))
        )
        return [
            tour_dto_factory(
                result["tour"][0] | {"lowest_price": result["min_price"]}
            )
            for result in results[0]["tours"]
        ], results[0]["count"][0]["total_results"] if results[0][
            "count"
        ] else 0

    def search_options(self) -> dict[str, Any]:
        fields = ["city", "country", "operator", "transport", "room_type"]

        return {
            field: self.tour_collection.distinct(field) for field in fields
        }


class TourView(ITourView):
    def __init__(self, mongo_client: MongoReadOnlyClient) -> None:
        self.tour_collection: "Collection" = mongo_client.get_db()[
            Collections.tour
        ]

    def get(self, tour_id: UUID) -> Optional[TourDto]:
        try:
            tour = list(self.tour_collection.find({"id": str(tour_id)}))[0]
            return tour_dto_factory(tour)
        except IndexError:
            return None
