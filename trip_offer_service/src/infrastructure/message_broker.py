import json
from datetime import datetime
from json import JSONEncoder
from typing import TYPE_CHECKING, Any
from uuid import UUID

from pika.exceptions import ChannelWrongStateError

if TYPE_CHECKING:
    from pika import BlockingConnection

    from src.consts import EXCHANGES


class ClassJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, UUID):
            return o.hex
        if isinstance(o, datetime):
            return str(o)

        return o.__dict__


class RabbitMQPublisher:
    exchange: "EXCHANGES"
    encoder: type[JSONEncoder] = ClassJSONEncoder
    routing_key: str = ""

    def __init__(self, connection: "BlockingConnection") -> None:
        self.connection = connection
        self.channel = connection.channel()

    def _channel_reconnect(self) -> None:
        self.channel = self.connection.channel()

    def _serialize(self, data: Any) -> bytes:
        return json.dumps(data, cls=self.encoder).encode("utf-8")

    def publish(self, data: Any) -> None:
        if self.channel.is_closed:
            self._channel_reconnect()

        payload = self._serialize(data)
        self.channel.basic_publish(
            exchange=self.exchange.value,
            routing_key=self.routing_key,
            body=payload,
        )
