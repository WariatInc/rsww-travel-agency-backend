from injector import Binder

from src.di_container.injector import Module
from src.offers.domain.ports import (
    IGetOfferEnrichmentDataQuery,
    IOffersView,
    IQueryCountOffers,
    IQueryOffer,
    IQuerySearchOffers,
    IQuerySearchOptions,
)
from src.offers.domain.queries import (
    CountOffersQuery,
    GetOfferEnrichmentDataQuery,
    InspectOfferQuery,
    SearchOffersQuery,
    SearchOptionsQuery,
)
from src.offers.infrastructure.storage.views import OffersView


class OffersModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(IOffersView, OffersView)
        self.bind(IQueryCountOffers, CountOffersQuery)
        self.bind(IQuerySearchOptions, SearchOptionsQuery)
        self.bind(IQuerySearchOffers, SearchOffersQuery)
        self.bind(IQueryOffer, InspectOfferQuery)
        self.bind(IGetOfferEnrichmentDataQuery, GetOfferEnrichmentDataQuery)