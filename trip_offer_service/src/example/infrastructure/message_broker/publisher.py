from src.consts import EXCHANGES
from src.infrastructure.message_broker import RabbitMQPublisher


class ExamplePublisher(RabbitMQPublisher):
    exchange = EXCHANGES.example
