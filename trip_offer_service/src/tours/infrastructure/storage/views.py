import re
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID

import pymongo

from src.consts import Collections, SortOrder, TourSort, TransportType
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

    def _search_offers(
        self,
        number_of_adults: Optional[int] = None,
        number_of_kids: Optional[int] = None,
    ) -> dict:
        query = {"is_available": True}

        if number_of_adults is not None:
            query["number_of_adults"] = number_of_adults
        if number_of_kids is not None:
            query["number_of_kids"] = number_of_kids

        return {
            result.get("_id"): result.get("min_price")
            for result in list(
                self.offer_collection.aggregate(
                    [
                        {"$match": query},
                        {
                            "$group": {
                                "_id": "$tour_id",
                                "min_price": {"$min": "$price"},
                            }
                        },
                    ]
                )
            )
        }

    def _search_tours(
        self,
        tours_ids: list[str],
        departure_city: Optional[str] = None,
        date_end: Optional[datetime] = None,
        date_start: Optional[datetime] = None,
        country: Optional[str] = None,
        operator: Optional[str] = None,
        transport: Optional[TransportType] = None,
        sort_by: Optional[TourSort] = None,
        sort_order: SortOrder = SortOrder.asc,
    ):
        query = {"id": {"$in": tours_ids}}

        if departure_city:
            query["departure_city"] = self._ilike_condition(departure_city)
        if country:
            query["country"] = self._ilike_condition(country)
        if operator:
            query["operator"] = self._ilike_condition(operator)
        if date_end:
            query["departure_date"] = {
                "$lt": datetime.combine(date_end, datetime.min.time())
            }
        if date_start:
            query["arrival_date"] = {
                "$gt": datetime.combine(date_start, datetime.min.time())
            }
        if transport:
            query["transport"] = transport

        result = self.tour_collection.find(query)

        order = (
            pymongo.ASCENDING
            if sort_order == SortOrder.asc
            else pymongo.DESCENDING
        )
        if sort_by == TourSort.arrival_date:
            result = result.sort("arrival_date", order)

        return list(result)

    def search(self, options: SearchOptions) -> tuple[list[TourDto], int]:
        tour_min_price_map = self._search_offers(options.adults, options.kids)
        tours = self._search_tours(
            list(tour_min_price_map),
            departure_city=options.departure_city,
            date_end=options.date_end,
            date_start=options.date_start,
            operator=options.operator,
            country=options.country,
            transport=options.transport,
            sort_by=options.sort_by,
        )
        tours_dto = [
            tour_dto_factory(
                tour | {"lowest_price": tour_min_price_map[tour["id"]]}
            )
            for tour in tours
        ]
        if options.sort_by == TourSort.price:
            order = SortOrder.desc == options.sort_order
            tours_dto = sorted(
                tours_dto, key=lambda x: x.lowest_price, reverse=order
            )

        start_index = (options.page - 1) * options.page_size
        return tours_dto[start_index: start_index + options.page_size], len(
            tours
        )

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
