from injector import Binder, provider, singleton

from src.di_container.modules import Module
from src.infrastructure.message_broker import RabbitMQConnectionFactory
from src.offer.domain.commands import (
    OfferReservationCommand,
    RandomizeOfferCommand,
    RandomizeTourCommand,
    UpdateOfferCommand,
    UpdateTourCommand,
)
from src.offer.domain.ports import (
    IGetOfferPriceQuery,
    IOfferPriceView,
    IOfferReservationCommand,
    IOfferUnitOfWork,
    IRandomizeOfferCommand,
    IRandomizeTourCommand,
    ITourUnitOfWork,
    IUpdateOfferCommand,
    IUpdateTourCommand,
)
from src.offer.domain.queries import GetOfferPriceQuery
from src.offer.infrastructure.message_broker.producer import (
    OfferPublisher,
    ReservationPublisher,
)
from src.offer.infrastructure.storage.unit_of_work import (
    OfferUnitOfWork,
    TourUnitOfWork,
)
from src.offer.infrastructure.storage.views import OfferPriceView


class OfferModule(Module):
    def configure(self, binder: Binder) -> None:
        # commands
        self.bind(IUpdateOfferCommand, UpdateOfferCommand)
        self.bind(IOfferReservationCommand, OfferReservationCommand)
        self.bind(IRandomizeOfferCommand, RandomizeOfferCommand)
        self.bind(IUpdateTourCommand, UpdateTourCommand)
        self.bind(IRandomizeTourCommand, RandomizeTourCommand)

        # queries
        self.bind(IGetOfferPriceQuery, GetOfferPriceQuery)

        # views
        self.bind(IOfferPriceView, OfferPriceView)

        # units of works
        self.bind(IOfferUnitOfWork, OfferUnitOfWork)
        self.bind(ITourUnitOfWork, TourUnitOfWork)

    @provider
    @singleton
    def provide_offer_publisher(
        self, rabbitmq_connection_factory: RabbitMQConnectionFactory
    ) -> OfferPublisher:
        return OfferPublisher(rabbitmq_connection_factory)

    @provider
    @singleton
    def provide_reservation_publisher(
        self, rabbitmq_connection_factory: RabbitMQConnectionFactory
    ) -> ReservationPublisher:
        return ReservationPublisher(rabbitmq_connection_factory)
