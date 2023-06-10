from injector import Binder

from src.di_container.injector import Module
from src.tours.domain.ports import (
    IGetTourQuery,
    IQueryCountTours,
    IQuerySearchOptions,
    IQuerySearchTours,
    IToursView,
    ITourView,
)
from src.tours.domain.queries import (
    CountToursQuery,
    GetTourQuery,
    SearchOptionsQuery,
    SearchToursQuery,
)
from src.tours.infrastructure.storage.views import ToursView, TourView


class ToursModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(IToursView, ToursView)
        self.bind(IQueryCountTours, CountToursQuery)
        self.bind(IQuerySearchOptions, SearchOptionsQuery)
        self.bind(IQuerySearchTours, SearchToursQuery)
        self.bind(ITourView, TourView)
        self.bind(IGetTourQuery, GetTourQuery)
