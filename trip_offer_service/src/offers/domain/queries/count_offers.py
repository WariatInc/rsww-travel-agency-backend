from src.offers.domain.dtos import SearchOptions
from src.offers.domain.ports import IOffersView, IQueryCountOffers


class CountOffersQuery(IQueryCountOffers):
    def __init__(self, view: IOffersView) -> None:
        self.view = view

    def __call__(self, options: SearchOptions) -> int:
        return self.view.count(options)
