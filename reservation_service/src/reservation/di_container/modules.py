from injector import Binder, provider, singleton

from src.di_container.injector import Module
from src.infrastructure.message_broker import RabbitMQConnectionFactory
from src.reservation.api import ReservationsResource
from src.reservation.domain.commands import (
    CancelReservationCommand,
    CreateReservationCommand,
    UpdateReservationCommand,
)
from src.reservation.domain.ports import (
    ICancelReservationCommand,
    ICreateReservationCommand,
    IGetUserReservationsQuery,
    IReservationListView,
    IReservationUnitOfWork,
    IUpdateReservationCommand,
)
from src.reservation.domain.queries import GetUserReservationQuery
from src.reservation.infrastructure.message_broker.producer import (
    ReservationPublisher,
)
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
        self.bind(IUpdateReservationCommand, UpdateReservationCommand)

        # Queries
        self.bind(IGetUserReservationsQuery, GetUserReservationQuery)

        # Unit of works
        self.bind(IReservationUnitOfWork, ReservationUnitOfWork)

        # Views
        self.bind(IReservationListView, ReservationListView)

    @provider
    @singleton
    def provide_reservation_publisher(
        self, connection_factory: RabbitMQConnectionFactory
    ) -> ReservationPublisher:
        return ReservationPublisher(connection_factory)
