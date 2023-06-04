from src.offers.domain.ports import IQuerySearchOffers, IOffersView
from src.offer.domain.dtos import OfferDto
from src.offers.domain.dtos import SearchOptions


class SearchOffersQuery(IQuerySearchOffers):
    def __init__(self, view: IOffersView) -> None:
        self.view = view

    def __call__(self, options: SearchOptions) -> list[OfferDto]:
        return self.view.search(options)
