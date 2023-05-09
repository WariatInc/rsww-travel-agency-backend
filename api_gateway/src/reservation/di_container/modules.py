from injector import Binder
from src.di_container.injector import Module
from src.reservation.api import ReservationsResource


class ReservationModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(ReservationsResource)
