from src.tours.domain.dtos import SearchOptions
from src.tours.domain.ports import IQueryCountTours, IToursView


class CountToursQuery(IQueryCountTours):
    def __init__(self, view: IToursView) -> None:
        self.view = view

    def __call__(self, options: SearchOptions) -> int:
        return self.view.count(options)
