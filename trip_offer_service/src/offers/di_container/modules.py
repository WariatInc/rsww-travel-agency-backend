from injector import Binder

from src.di_container.injector import Module
from src.offers.domain.ports import (
    IGetOfferEnrichmentDataQuery,
    IOfferRepository,
    IOffersView,
    IQueryCountOffers,
    IQueryOffer,
    IQuerySearchOffers,
    IQuerySearchOptions,
    IUpdateOffer,
)
from src.offers.domain.queries import (
    CountOffersQuery,
    GetOfferEnrichmentDataQuery,
    InspectOfferQuery,
    SearchOffersQuery,
    SearchOptionsQuery,
)
from src.offers.domain.upserts import UpdateOffer
from src.offers.infrastructure.storage.repository import OfferRepository
from src.offers.infrastructure.storage.views import OffersView


class OffersModule(Module):
    def configure(self, binder: Binder) -> None:
        # Views
        self.bind(IOffersView, OffersView)

        # Repositories
        self.bind(IOfferRepository, OfferRepository)

        # Queries
        self.bind(IQueryCountOffers, CountOffersQuery)
        self.bind(IQuerySearchOptions, SearchOptionsQuery)
        self.bind(IQuerySearchOffers, SearchOffersQuery)
        self.bind(IQueryOffer, InspectOfferQuery)
        self.bind(IGetOfferEnrichmentDataQuery, GetOfferEnrichmentDataQuery)

        # Upserts
        self.bind(IUpdateOffer, UpdateOffer)
