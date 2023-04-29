from src.consts import Exchanges
from src.infrastructure.message_broker import RabbitMQPublisher


class ExamplePublisher(RabbitMQPublisher):
    exchange = Exchanges.example
