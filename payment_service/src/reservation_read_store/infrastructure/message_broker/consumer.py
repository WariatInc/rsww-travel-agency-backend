import json
import logging
from typing import TYPE_CHECKING, Any

from flask import Config

from src.config import DefaultConfig
from src.consts import Queues
from src.infrastructure.message_broker import (
    RabbitMQConnectionFactory,
    RabbitMQConsumer,
)
from src.infrastructure.storage import SessionFactory, SQLAlchemyEngine
from src.reservation_read_store.domain.commands import (
    ReservationReadStoreSynchronizationCommand,
)
from src.reservation_read_store.domain.events import (
    ReservationCreatedEvent,
    ReservationUpdatedEvent,
)
from src.reservation_read_store.domain.ports import (
    IReservationReadStoreSynchronizationCommand,
)
from src.reservation_read_store.infrastructure.storage.unit_of_work import (
    ReservationReadStoreUnitOfWork,
)

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import (
        BlockingChannel,
        BlockingConnection,
    )
    from pika.spec import Basic, BasicProperties


class ReservationConsumer(RabbitMQConsumer):
    queue = Queues.payment_service_reservation_queue

    def __init__(
        self,
        connection: "BlockingConnection",
        reservation_read_store_synchronization_command: IReservationReadStoreSynchronizationCommand,
    ) -> None:
        self._reservation_read_store_synchronization_command = (
            reservation_read_store_synchronization_command
        )
        super().__init__(connection)

    def _consume_reservation_created_event(
        self, payload: dict[str, str]
    ) -> None:
        event = ReservationCreatedEvent.from_rabbitmq_message(payload)
        logger.info(msg=f"Consuming event: {event.type} with id: {event.id}")
        self._reservation_read_store_synchronization_command(
            reservation_id=event.reservation_id, state=event.state
        )
        logger.info(msg=f"Event with id: {event.id} successfully consumed")

    def _consume_reservation_updated_event(
        self, payload: dict[str, Any]
    ) -> None:
        event = ReservationUpdatedEvent.from_rabbitmq_message(payload)
        logger.info(msg=f"Consuming event: {event.type} with id: {event.id}")
        if event.state:
            self._reservation_read_store_synchronization_command(
                reservation_id=event.reservation_id, state=event.state
            )
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

        elif event_payload.get("type") == ReservationUpdatedEvent.__name__:
            self._consume_reservation_updated_event(event_payload)

        self.channel.basic_ack(delivery_tag=method.delivery_tag)


def _consume() -> None:
    config = Config("")
    config.from_object(DefaultConfig)

    connection_factory = RabbitMQConnectionFactory(config)
    session_factory = SessionFactory(SQLAlchemyEngine(config))

    reservation_read_store_synchronization_command = (
        ReservationReadStoreSynchronizationCommand(
            ReservationReadStoreUnitOfWork(session_factory)
        )
    )

    consumer = ReservationConsumer(
        connection_factory.create_connection(),
        reservation_read_store_synchronization_command,
    )

    logger.info(msg="Start consuming")
    consumer.consume()


if __name__ == "__main__":
    logging.basicConfig(
        format="Payment service reservation consumer | %(name)s - %(levelname)s - %(asctime)s - %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    _consume()
