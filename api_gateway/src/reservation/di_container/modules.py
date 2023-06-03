from injector import Binder

from src.di_container.injector import Module
from src.reservation.api import (
    ReservationCancelResource,
    ReservationEventDashboardResource,
    ReservationResource,
    ReservationsResource,
)


class ReservationModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(ReservationsResource)
        self.bind(ReservationCancelResource)
        self.bind(ReservationResource)
        self.bind(ReservationEventDashboardResource)
