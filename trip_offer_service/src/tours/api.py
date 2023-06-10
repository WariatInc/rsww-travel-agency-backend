from http import HTTPStatus
from math import ceil
from uuid import UUID

from flask import jsonify
from webargs.flaskparser import use_args

from src.api import Resource
from src.api.blueprint import Blueprint
from src.api.error import custom_error
from src.api.schema import use_schema
from src.tours.domain.dtos import SearchOptions
from src.tours.domain.exceptions import TourNotFoundException
from src.tours.domain.ports import (
    IGetTourQuery,
    IQueryCountTours,
    IQuerySearchOptions,
    IQuerySearchTours,
)
from src.tours.errors import ERROR
from src.tours.schema import SearchOptionsSchema, TourSchema


class SearchResource(Resource):
    def __init__(
        self, search: IQuerySearchTours, count_tours: IQueryCountTours
    ) -> None:
        self.search = search
        self.count_tours = count_tours

    @use_args(SearchOptionsSchema, location="query")
    def get(self, options: SearchOptions):
        tour_schema = TourSchema(many=True)
        tours = tour_schema.dump(self.search(options))
        number_of_tours = self.count_tours(options)
        return jsonify(
            max_page=ceil(number_of_tours / options.page_size),
            result=tours,
        )


class SearchOptionsResource(Resource):
    def __init__(self, get_search_options: IQuerySearchOptions) -> None:
        self.get_search_options = get_search_options

    def get(self):
        return jsonify(self.get_search_options())


class TourResource(Resource):
    def __init__(self, get_tour_query: IGetTourQuery) -> None:
        self.get_tour_query = get_tour_query

    @use_schema(TourSchema, HTTPStatus.OK)
    def get(self, tour_id: UUID):
        try:
            return self.get_tour_query.get(tour_id)
        except TourNotFoundException:
            return custom_error(
                ERROR.tour_not_found_error, HTTPStatus.NOT_FOUND
            )


class Api(Blueprint):
    name = "tours"
    import_name = __name__

    resources = [
        (TourResource, "/<uuid:tour_id>"),
        (SearchResource, "/search"),
        (SearchOptionsResource, "/search/options"),
    ]
