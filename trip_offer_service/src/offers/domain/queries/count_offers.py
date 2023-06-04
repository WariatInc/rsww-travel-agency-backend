from src.offers.domain.ports import IQueryCountOffers, IOffersView
from src.offers.domain.dtos import SearchOptions


class CountOffersQuery(IQueryCountOffers):
    def __init__(self, view: IOffersView) -> None:
        self.view = view

    def __call__(self, options: SearchOptions) -> int:
        return self.view.count(options)
