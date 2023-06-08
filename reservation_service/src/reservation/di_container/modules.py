from injector import Binder, provider, singleton

from src.di_container.injector import Module
from src.infrastructure.message_broker import RabbitMQConnectionFactory
from src.reservation.api import (
    ReservationCancelResource,
    ReservationResource,
    ReservationsResource,
)
from src.reservation.domain.commands import (
    CancelReservationCommand,
    CreateReservationCommand,
    DeleteRejectedReservationCommand,
    UpdateReservationCommand,
    UpdateReservationEventDashboardCommand,
)
from src.reservation.domain.ports import (
    ICancelReservationCommand,
    ICreateReservationCommand,
    IDeleteRejectedReservationCommand,
    IGetReservationEventDashboardListQuery,
    IGetReservationQuery,
    IGetUserReservationsQuery,
    IReservationEventDashboardListView,
    IReservationEventDashboardUnitOfWork,
    IReservationListView,
    IReservationsToCancelView,
    IReservationUnitOfWork,
    IReservationView,
    IUpdateReservationCommand,
    IUpdateReservationEventDashboardCommand,
)
from src.reservation.domain.queries import (
    GetReservationEventDashboardListQuery,
    GetReservationQuery,
    GetUserReservationsQuery,
)
from src.reservation.infrastructure.message_broker.producer import (
    ReservationPublisher,
)
from src.reservation.infrastructure.storage.unit_of_work import (
    ReservationEventDashboardUnitOfWork,
    ReservationUnitOfWork,
)
from src.reservation.infrastructure.storage.views import (
    ReservationEventDashboardListView,
    ReservationListView,
    ReservationsToCancelView,
    ReservationView,
)


class ReservationModule(Module):
    def configure(self, binder: Binder) -> None:
        # Resources
        self.bind(ReservationsResource)
        self.bind(ReservationResource)
        self.bind(ReservationCancelResource)

        # Commands
        self.bind(ICreateReservationCommand, CreateReservationCommand)
        self.bind(ICancelReservationCommand, CancelReservationCommand)
        self.bind(IUpdateReservationCommand, UpdateReservationCommand)
        self.bind(
            IDeleteRejectedReservationCommand, DeleteRejectedReservationCommand
        )
        self.bind(
            IUpdateReservationEventDashboardCommand,
            UpdateReservationEventDashboardCommand,
        )

        # Queries
        self.bind(IGetUserReservationsQuery, GetUserReservationsQuery)
        self.bind(IGetReservationQuery, GetReservationQuery)
        self.bind(
            IGetReservationEventDashboardListQuery,
            GetReservationEventDashboardListQuery,
        )

        # Unit of works
        self.bind(IReservationUnitOfWork, ReservationUnitOfWork)
        self.bind(
            IReservationEventDashboardUnitOfWork,
            ReservationEventDashboardUnitOfWork,
        )

        # Views
        self.bind(IReservationListView, ReservationListView)
        self.bind(IReservationView, ReservationView)
        self.bind(
            IReservationEventDashboardListView,
            ReservationEventDashboardListView,
        )
        self.bind(IReservationsToCancelView, ReservationsToCancelView)

    @provider
    @singleton
    def provide_reservation_publisher(
        self, connection_factory: RabbitMQConnectionFactory
    ) -> ReservationPublisher:
        return ReservationPublisher(connection_factory)
