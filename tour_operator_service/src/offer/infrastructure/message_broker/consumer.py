import json
import logging
from typing import TYPE_CHECKING, Any, Optional

from src.config import Config, DefaultConfig
from src.consts import Queues
from src.infrastructure.message_broker import (RabbitMQConnectionFactory,
                                               RabbitMQConsumer)
from src.infrastructure.storage import SessionFactory, SQLAlchemyEngine
from src.offer.domain.commands import (OfferReservationCommand,
                                       UpdateOfferCommand)
from src.offer.domain.events import (ReservationCancelledEvent,
                                     ReservationCreatedEvent)
from src.offer.domain.ports import (IOfferReservationCommand,
                                    IUpdateOfferCommand)
from src.offer.infrastructure.message_broker.producer import (
    OfferPublisher, ReservationPublisher)
from src.offer.infrastructure.storage.unit_of_work import OfferUnitOfWork

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import (BlockingChannel,
                                                   BlockingConnection)
    from pika.spec import Basic, BasicProperties


logging.basicConfig(
    format="%(name)s - %(levelname)s - %(asctime)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("Reservation Consumer")


class ReservationConsumer(RabbitMQConsumer):
    queue = Queues.tour_operator_reservation_queue

    def __init__(
        self,
        connection: "BlockingConnection",
        update_offer_command: IUpdateOfferCommand,
        offer_reservation_command: IOfferReservationCommand,
    ) -> None:
        self._update_offer_command = update_offer_command
        self._offer_reservation_command = offer_reservation_command
        super().__init__(connection)

    def _consume_reservation_created_event(
        self, payload: dict[str, Any]
    ) -> None:
        event = ReservationCreatedEvent.from_rabbitmq_message(payload)
        logger.info(msg=f"Consuming event: {event.type} with id: {event.id}")
        self._offer_reservation_command(event.offer_id, event.reservation_id)
        logger.info(msg=f"Event with id: {event.id} successfully consumed")

    def _consume_reservation_cancelled_event(
        self, payload: dict[str, Any]
    ) -> None:
        event = ReservationCancelledEvent.from_rabbitmq_message(payload)
        logger.info(msg=f"Consuming event: {event.type} with id: {event.id}")
        self._update_offer_command(event.offer_id, available=True)
        logger.info(msg=f"Event with id: {event.id} successfully consumed")

    def _callback(
        self,
        channel: "BlockingChannel",
        method: "Basic.Deliver",
        properties: "BasicProperties",
        body: bytes,
    ) -> None:
        event_payload = json.loads(body.decode())
        if event_payload.get("type") == ReservationCreatedEvent.__name__:
            self._consume_reservation_created_event(event_payload)

        elif event_payload.get("type") == ReservationCancelledEvent.__name__:
            self._consume_reservation_cancelled_event(event_payload)

        self.channel.basic_ack(delivery_tag=method.delivery_tag)


def consume(config: Optional[type[Config]] = None) -> None:
    if not config:
        config = DefaultConfig

    connection_factory = RabbitMQConnectionFactory(config)
    session_factory = SessionFactory(SQLAlchemyEngine(config))

    update_offer_command = UpdateOfferCommand(
        uow=OfferUnitOfWork(session_factory),
        publisher=OfferPublisher(connection_factory),
    )
    offer_reservation_command = OfferReservationCommand(
        uow=OfferUnitOfWork(session_factory),
        update_offer_command=update_offer_command,
        publisher=ReservationPublisher(connection_factory),
    )
    consumer = ReservationConsumer(
        connection_factory.create_connection(),
        update_offer_command,
        offer_reservation_command,
    )

    logger.info(msg="Start consuming")
    consumer.consume()


if __name__ == "__main__":
    consume()
