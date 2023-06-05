from typing import Any

from src.tours.domain.ports import IQuerySearchOptions, IToursView


class SearchOptionsQuery(IQuerySearchOptions):
    def __init__(self, view: IToursView) -> None:
        self.view = view

    def __call__(self) -> dict[str, Any]:
        return self.view.search_options()
