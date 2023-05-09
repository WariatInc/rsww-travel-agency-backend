import json
import logging
from typing import TYPE_CHECKING, Optional

from flask import Config

from src.config import DefaultConfig
from src.consts import Queues, ReservationState
from src.infrastructure.message_broker import (
    RabbitMQConnectionFactory,
    RabbitMQConsumer,
)
from src.infrastructure.storage import SessionFactory, SQLAlchemyEngine
from src.payment.domain.events import ItemPaidEvent
from src.reservation.domain.commands import UpdateReservationCommand
from src.reservation.domain.ports import IUpdateReservationCommand
from src.reservation.infrastructure.message_broker.producer import (
    ReservationPublisher,
)
from src.reservation.infrastructure.storage.unit_of_work import (
    ReservationUnitOfWork,
)

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import (
        BlockingChannel,
        BlockingConnection,
    )
    from pika.spec import Basic, BasicProperties


logging.basicConfig(
    format="%(name)s - %(levelname)s - %(asctime)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("Payment Consumer")


class PaymentConsumer(RabbitMQConsumer):
    queue = Queues.reservation_service_payment_queue

    def __init__(
        self,
        connection: "BlockingConnection",
        update_reservation_command: IUpdateReservationCommand,
    ) -> None:
        self._update_reservation_command = update_reservation_command
        super().__init__(connection)

    def _consume_item_paid_event(self, payload: dict[str, str]) -> None:
        event = ItemPaidEvent.from_rabbitmq_message(payload)
        logger.info(msg=f"Consuming event: {event.type} with id: {event.id}")
        if event.item_type == "reservation":
            self._update_reservation_command(
                event.item_id, state=ReservationState.paid
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
        if event_payload.get("type") == ItemPaidEvent.__name__:
            self._consume_item_paid_event(event_payload)

        self.channel.basic_ack(delivery_tag=method.delivery_tag)


def consume(config: Optional[Config] = None) -> None:
    if not config:
        config = Config("")
        config.from_object(DefaultConfig)

    connection_factory = RabbitMQConnectionFactory(config)
    session_factory = SessionFactory(SQLAlchemyEngine(config))

    update_reservation_command = UpdateReservationCommand(
        uow=ReservationUnitOfWork(session_factory),
        publisher=ReservationPublisher(connection_factory),
    )

    consumer = PaymentConsumer(
        connection_factory.create_connection(), update_reservation_command
    )

    logger.info(msg="Start consuming")
    consumer.consume()


if __name__ == "__main__":
    consume()
