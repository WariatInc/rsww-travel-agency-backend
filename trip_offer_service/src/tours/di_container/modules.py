from injector import Binder

from src.di_container.injector import Module
from src.tours.domain.ports import (
    IQueryCountTours,
    IQuerySearchOptions,
    IQuerySearchTours,
    IToursView,
)
from src.tours.domain.queries import (
    CountToursQuery,
    SearchToursQuery,
    SearchOptionsQuery,
)
from src.tours.infrastructure.storage.views import ToursView


class ToursModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(IToursView, ToursView)
        self.bind(IQueryCountTours, CountToursQuery)
        self.bind(IQuerySearchOptions, SearchOptionsQuery)
        self.bind(IQuerySearchTours, SearchToursQuery)
