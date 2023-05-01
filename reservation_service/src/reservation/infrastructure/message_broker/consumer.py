import json
import logging
from typing import TYPE_CHECKING

from flask import Config

from src.config import DefaultConfig
from src.consts import Queues
from src.infrastructure.message_broker import (
    RabbitMQConnectionFactory,
    RabbitMQConsumer,
)
from src.infrastructure.storage import SessionFactory, SQLAlchemyEngine
from src.reservation.domain.commands import UpdateReservationCommand
from src.reservation.domain.events import ReservationCheckedEvent
from src.reservation.domain.ports import IUpdateReservationCommand
from src.reservation.infrastructure.storage.unit_of_work import (
    ReservationUnitOfWork,
)

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import (
        BlockingChannel,
        BlockingConnection,
    )
    from pika.spec import Basic, BasicProperties


class ReservationConsumer(RabbitMQConsumer):
    queue = Queues.reservation_service_reservation_queue

    def __init__(
        self,
        connection: "BlockingConnection",
        update_reservation_command: IUpdateReservationCommand,
    ) -> None:
        self._update_reservation_command = update_reservation_command
        super().__init__(connection)

    def _callback(
        self,
        channel: "BlockingChannel",
        method: "Basic.Deliver",
        properties: "BasicProperties",
        body: bytes,
    ) -> None:
        event_payload = json.loads(body.decode())
        if event_payload.get("type") == ReservationCheckedEvent.__name__:
            event = ReservationCheckedEvent.from_rabbitmq_message(
                event_payload
            )
            logger.info(
                msg=f"Consuming event: {event.type} with id: {event.id}"
            )
            self._update_reservation_command(
                event.reservation_id, state=event.reservation_state
            )
            logger.info(msg=f"Event with id: {event.id} successfully consumed")

        self.channel.basic_ack(delivery_tag=method.delivery_tag)


def _consume() -> None:
    config = Config("")
    config.from_object(DefaultConfig)

    connection_factory = RabbitMQConnectionFactory(config)
    session_factory = SessionFactory(SQLAlchemyEngine(config))

    update_reservation_command = UpdateReservationCommand(
        ReservationUnitOfWork(session_factory)
    )

    consumer = ReservationConsumer(
        connection_factory.create_connection(), update_reservation_command
    )

    logger.info(msg="Start consuming")
    consumer.consume()


if __name__ == "__main__":
    logging.basicConfig(
        format="Reservation service reservation consumer | %(name)s - %(levelname)s - %(asctime)s - %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    _consume()
