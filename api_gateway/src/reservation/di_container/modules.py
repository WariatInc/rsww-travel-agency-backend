from injector import Binder

from src.di_container.injector import Module
from src.reservation.api import (
    ReservationCancelResource,
    ReservationEventDashboardResource,
    ReservationResource,
    ReservationsResource,
)
from src.reservation.domian.commands import (
    EnrichReservationsWithOffersDataCommand,
)
from src.reservation.domian.ports import (
    IEnrichReservationsWithOffersDataCommand,
)


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
