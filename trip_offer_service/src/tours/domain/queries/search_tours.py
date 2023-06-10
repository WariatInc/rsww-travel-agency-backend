from src.tours.domain.dtos import SearchOptions, TourDto
from src.tours.domain.ports import IQuerySearchTours, IToursView


class SearchToursQuery(IQuerySearchTours):
    def __init__(self, view: IToursView) -> None:
        self.view = view

    def __call__(self, options: SearchOptions) -> tuple[list[TourDto], int]:
        return self.view.search(options)
