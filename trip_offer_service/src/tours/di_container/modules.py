from injector import Binder

from src.di_container.injector import Module
from src.tours.domain.commands import UpsertTourCommand
from src.tours.domain.ports import (
    IGetTourQuery,
    IQuerySearchOptions,
    IQuerySearchTours,
    ITourRepository,
    IToursView,
    ITourView,
    IUpsertTourCommand,
)
from src.tours.domain.queries import (
    GetTourQuery,
    SearchOptionsQuery,
    SearchToursQuery,
)
from src.tours.infrastructure.storage.repository import TourRepository
from src.tours.infrastructure.storage.views import ToursView, TourView


class ToursModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(IToursView, ToursView)
        self.bind(IQuerySearchOptions, SearchOptionsQuery)
        self.bind(IQuerySearchTours, SearchToursQuery)
        self.bind(ITourView, TourView)
        self.bind(IGetTourQuery, GetTourQuery)
        self.bind(ITourRepository, TourRepository)
        self.bind(IUpsertTourCommand, UpsertTourCommand)
