import json
from abc import abstractmethod
from datetime import datetime
from json import JSONEncoder
from typing import TYPE_CHECKING, Any
from uuid import UUID

from pika import (BasicProperties, BlockingConnection, ConnectionParameters,
                  PlainCredentials)
from pika.exceptions import StreamLostError
from pika.spec import PERSISTENT_DELIVERY_MODE
from src.config import Config

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic
    from src.consts import Exchanges, Queues


class ClassJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, UUID):
            return o.hex
        if isinstance(o, datetime):
            return str(o)

        return o.__dict__


class RabbitMQConnectionFactory:
    def __init__(self, config: Config) -> None:
        self._config = config

    def create_connection(self) -> BlockingConnection:
        credentials = PlainCredentials(
            self._config.RABBITMQ_USER,
            self._config.RABBITMQ_PASSWORD,
        )
        parameters = ConnectionParameters(
            host=self._config.RABBITMQ_HOST,
            port=self._config.RABBITMQ_PORT,
            credentials=credentials,
        )
        return BlockingConnection(parameters)


class RabbitMQPublisher:
    exchange: "Exchanges"
    encoder: type[JSONEncoder] = ClassJSONEncoder
    routing_key: str = ""

    def __init__(self, connection_factory: RabbitMQConnectionFactory) -> None:
        self.connection_factory = connection_factory
        self.connection = self.connection_factory.create_connection()
        self.channel = self.connection.channel()

    def _reconnect(self) -> None:
        self.connection = self.connection_factory.create_connection()
        self.channel = self.connection.channel()

    def _serialize(self, data: Any) -> bytes:
        return json.dumps(data, cls=self.encoder).encode("utf-8")

    def publish(self, data: Any) -> None:
        payload = self._serialize(data)
        try:
            self.channel.basic_publish(
                exchange=self.exchange.value,
                routing_key=self.routing_key,
                body=payload,
                properties=BasicProperties(
                    delivery_mode=PERSISTENT_DELIVERY_MODE
                ),
            )
        except StreamLostError:
            self._reconnect()
            self.publish(data)


class RabbitMQConsumer:
    queue: "Queues"

    def __init__(self, connection: BlockingConnection) -> None:
        self.channel = connection.channel()

    @abstractmethod
    def _callback(
        self,
        channel: "BlockingChannel",
        method: "Basic.Deliver",
        properties: "BasicProperties",
        body: bytes,
    ) -> None:
        raise NotImplementedError

    def consume(self) -> None:
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self._callback,
            auto_ack=False,
        )
        self.channel.start_consuming()
