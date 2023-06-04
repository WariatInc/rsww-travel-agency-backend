from typing import Any
from src.tours.domain.ports import IToursView, IQuerySearchOptions


class SearchOptionsQuery(IQuerySearchOptions):
    def __init__(self, view: IToursView) -> None:
        self.view = view

    def __call__(self) -> dict[str, Any]:
        return self.view.search_options()
