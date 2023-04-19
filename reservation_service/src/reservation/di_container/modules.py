from injector import Binder

from src.di_container.injector import Module
from src.reservation.api import ReservationsResource
from src.reservation.domain.commands import (
    CancelReservationCommand,
    CreateReservationCommand,
)
from src.reservation.domain.ports import (
    ICancelReservationCommand,
    ICreateReservationCommand,
    IGetUserReservationsQuery,
    IReservationListView,
    IReservationUnitOfWork,
)
from src.reservation.domain.queries import GetUserReservationQuery
from src.reservation.infrastructure.storage.unit_of_work import (
    ReservationUnitOfWork,
)
from src.reservation.infrastructure.storage.views import ReservationListView


class ReservationModule(Module):
    def configure(self, binder: Binder) -> None:
        # Resources
        self.bind(ReservationsResource)

        # Commands
        self.bind(ICreateReservationCommand, CreateReservationCommand)
        self.bind(ICancelReservationCommand, CancelReservationCommand)

        # Queries
        self.bind(IGetUserReservationsQuery, GetUserReservationQuery)

        # Unit of works
        self.bind(IReservationUnitOfWork, ReservationUnitOfWork)

        # Views
        self.bind(IReservationListView, ReservationListView)
