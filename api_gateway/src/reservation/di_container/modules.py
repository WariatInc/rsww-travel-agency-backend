from injector import Binder

from src.di_container.injector import Module
from src.reservation.api import (
    ReservationCancelResource,
    ReservationEventDashboardResource,
    ReservationResource,
    ReservationsResource,
)
from src.reservation.domain.commands import (
    EnrichReservationsWithOffersDataCommand,
)
from src.reservation.domain.ports import (
    IEnrichReservationsWithOffersDataCommand,
    IGetUsersPreferencesQuery,
)
from src.reservation.domain.queries import GetUsersPreferencesQuery


class ReservationModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(ReservationsResource)
        self.bind(ReservationCancelResource)
        self.bind(ReservationResource)
        self.bind(ReservationEventDashboardResource)
        self.bind(
            IEnrichReservationsWithOffersDataCommand,
            EnrichReservationsWithOffersDataCommand,
        )
        self.bind(IGetUsersPreferencesQuery, GetUsersPreferencesQuery)
