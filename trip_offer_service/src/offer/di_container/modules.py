from injector import Binder

from src.di_container.injector import Module
from src.offer.domain.ports import IGetOfferQuery, ISearchOfferQuery
from src.offer.domain.queries import GetOfferQuery, SearchOfferQuery


class OfferModule(Module):
    def configure(self, binder: Binder) -> None:
        # queries
        self.bind(IGetOfferQuery, GetOfferQuery)
        self.bind(ISearchOfferQuery, SearchOfferQuery)
