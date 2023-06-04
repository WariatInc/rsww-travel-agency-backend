from http import HTTPStatus
from uuid import UUID
from math import ceil

from flask import jsonify
from webargs.flaskparser import use_args

from src.tours.domain.ports import (
    IQuerySearchOptions,
    IQueryCountTours,
    IQuerySearchTours,
)
from src.tours.schema import SearchOptionsSchema
from src.tour.schema import TourSchema
from src.tours.domain.dtos import SearchOptions
from src.api.blueprint import Blueprint
from src.api import Resource


class SearchResource(Resource):
    def __init__(
        self, search: IQuerySearchTours, count_tours: IQueryCountTours
    ) -> None:
        self.search = search
        self.count_tours = count_tours

    @use_args(SearchOptionsSchema(), location="query")
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


class Api(Blueprint):
    name = "tours"
    import_name = __name__

    resources = [
        (SearchResource, "/search"),
        (SearchOptionsResource, "/search/options"),
    ]
