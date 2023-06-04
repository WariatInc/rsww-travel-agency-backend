import json
import logging
from typing import TYPE_CHECKING, Optional

from flask import Config

from src.config import DefaultConfig
from src.consts import Queues
from src.infrastructure.message_broker import (
    RabbitMQConnectionFactory,
    RabbitMQConsumer,
)
from src.infrastructure.storage import SessionFactory, SQLAlchemyEngine
from src.reservation.domain.commands import (
    UpdateReservationCommand,
    UpdateReservationEventDashboardCommand,
)
from src.reservation.domain.events import (
    ReservationCheckedEvent,
    ReservationCreatedEvent,
    ReservationEventDashboardUpdate,
    ReservationUpdatedEvent,
)
from src.reservation.domain.ports import (
    IUpdateReservationCommand,
    IUpdateReservationEventDashboardCommand,
)
from src.reservation.infrastructure.message_broker.producer import (
    ReservationPublisher,
)
from src.reservation.infrastructure.storage.unit_of_work import (
    ReservationEventDashboardUnitOfWork,
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
logger = logging.getLogger("Reservation Consumer")


class ReservationConsumer(RabbitMQConsumer):
    queue = Queues.reservation_service_reservation_queue

    def __init__(
        self,
        connection: "BlockingConnection",
        update_reservation_command: IUpdateReservationCommand,
        update_reservation_event_dashboard_command: IUpdateReservationEventDashboardCommand,
    ) -> None:
        self._update_reservation_command = update_reservation_command
        self._update_reservation_event_dashboard_command = (
            update_reservation_event_dashboard_command
        )
        super().__init__(connection)

    def _consume_reservation_checked_event(
        self, payload: dict[str, str]
    ) -> None:
        event = ReservationCheckedEvent.from_rabbitmq_message(payload)
        logger.info(msg=f"Consuming event: {event.type} with id: {event.id}")
        self._update_reservation_command(
            event.reservation_id,
            state=event.reservation_state,
            rejection_reason=event.rejection_reason,
            price=event.price,
        )
        logger.info(msg=f"Event with id: {event.id} successfully consumed")

    def _update_reservation_event_dashboard(
        self, payload: dict[str, str]
    ) -> None:
        event = ReservationEventDashboardUpdate.from_rabbitmq_message(payload)
        logger.info(msg=f"Consuming event: {event.type} with id: {event.id}")
        self._update_reservation_event_dashboard_command(
            reservation_event_id=event.id,
            timestamp=event.time,
            reservation_id=event.reservation_id,
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
        if event_payload.get("type") == ReservationCheckedEvent.__name__:
            self._consume_reservation_checked_event(event_payload)

        if event_payload.get("type") in [
            ReservationCreatedEvent.__name__,
            ReservationUpdatedEvent.__name__,
        ]:
            self._update_reservation_event_dashboard(event_payload)

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
    update_reservation_event_dashboard_command = (
        UpdateReservationEventDashboardCommand(
            uow=ReservationEventDashboardUnitOfWork(session_factory)
        )
    )

    consumer = ReservationConsumer(
        connection_factory.create_connection(),
        update_reservation_command,
        update_reservation_event_dashboard_command,
    )

    logger.info(msg="Start consuming")
    consumer.consume()


if __name__ == "__main__":
    consume()
