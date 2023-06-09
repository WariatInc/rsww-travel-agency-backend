import json
import logging
from math import ceil
from typing import TYPE_CHECKING, Any, Optional

from flask import Config

from src.config import DefaultConfig
from src.consts import PROVISION, Queues
from src.infrastructure.message_broker import (
    RabbitMQConnectionFactory,
    RabbitMQConsumer,
)
from src.infrastructure.storage import MongoClient
from src.offers.domain.events import OfferChangedEvent
from src.offers.domain.ports import IUpdateOffer
from src.offers.domain.upserts.update_offer import UpdateOffer
from src.offers.infrastructure.storage.repository import OfferRepository
from src.tours.domain.commands import UpsertTourCommand
from src.tours.domain.events import TourChangedEvent
from src.tours.domain.ports import IUpsertTourCommand
from src.tours.infrastructure.storage.repository import TourRepository

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
    queue = Queues.trip_offer_service_offer_queue

    def __init__(
        self,
        connection: "BlockingConnection",
        update_offer: IUpdateOffer,
        upsert_tour_command: IUpsertTourCommand,
    ) -> None:
        self.update_offer = update_offer
        self.upsert_tour_command = upsert_tour_command
        super().__init__(connection)

    def _consume_offer_changed_event(self, payload: dict[str, Any]) -> None:
        event = OfferChangedEvent.from_rabbitmq_message(payload)
        logger.info(msg=f"Consuming event: {event.type} with id: {event.id}")

        if "available" in event.details.keys():
            event.details["is_available"] = event.details.pop("available")

        event.details["price"] = (
            ceil(event.details["price"] * (1 + PROVISION)) - 0.01
        )
        self.update_offer(event.offer_id, **event.details)

        logger.info(msg=f"Event with id: {event.id} successfully consumed")

    def _consume_tour_changed_event(self, payload: dict[str, Any]) -> None:
        event = TourChangedEvent.from_rabbitmq_message(payload)
        logger.info(msg=f"Consuming event: {event.type} with id: {event.id}")
        self.upsert_tour_command(event.tour_id, **event.details)
        logger.info(msg=f"Event with id: {event.id} successfully consumed")

    def _callback(
        self,
        channel: "BlockingChannel",
        method: "Basic.Deliver",
        properties: "BasicProperties",
        body: bytes,
    ) -> None:
        event_payload = json.loads(body.decode())
        if event_payload.get("type") == OfferChangedEvent.__name__:
            self._consume_offer_changed_event(event_payload)

        if event_payload.get("type") == TourChangedEvent.__name__:
            self._consume_tour_changed_event(event_payload)

        self.channel.basic_ack(delivery_tag=method.delivery_tag)


def consume(config: Optional[type[Config]] = None) -> None:
    if not config:
        config = Config("")
        config.from_object(DefaultConfig)

    connection_factory = RabbitMQConnectionFactory(config)
    client = MongoClient(config)

    consumer = ReservationConsumer(
        connection_factory.create_connection(),
        UpdateOffer(OfferRepository(client)),
        UpsertTourCommand(TourRepository(client)),
    )

    logger.info(msg="Start consuming")
    consumer.consume()


if __name__ == "__main__":
    consume()
