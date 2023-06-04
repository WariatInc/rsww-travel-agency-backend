from typing import Any
from src.offers.domain.ports import IOffersView, IQuerySearchOptions


class SearchOptionsQuery(IQuerySearchOptions):
    def __init__(self, view: IOffersView) -> None:
        self.view = view

    def __call__(self) -> dict[str, Any]:
        return self.view.search_options()
