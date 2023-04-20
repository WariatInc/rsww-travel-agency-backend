from injector import Binder, provider, singleton
from pika import BlockingConnection

from src.di_container.modules import Module
from src.offer.domain.commands import (
    OfferReservationCommand,
    UpdateOfferCommand,
)
from src.offer.domain.ports import (
    IOfferReservationCommand,
    IOfferUnitOfWork,
    IUpdateOfferCommand,
)
from src.offer.infrastructure.message_broker.producer import (
    OfferPublisher,
    ReservationPublisher,
)
from src.offer.infrastructure.storage.unit_of_work import OfferUnitOfWork


class OfferModule(Module):
    def configure(self, binder: Binder) -> None:
        # commands
        self.bind(IUpdateOfferCommand, UpdateOfferCommand)
        self.bind(IOfferReservationCommand, OfferReservationCommand)

        # units of works
        self.bind(IOfferUnitOfWork, OfferUnitOfWork)

    @provider
    @singleton
    def provide_offer_publisher(
        self, connection: BlockingConnection
    ) -> OfferPublisher:
        return OfferPublisher(connection)

    @provider
    @singleton
    def provide_reservation_publisher(
        self, connection: BlockingConnection
    ) -> ReservationPublisher:
        return ReservationPublisher(connection)
