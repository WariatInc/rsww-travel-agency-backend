from src.consts import Exchanges
from src.infrastructure.message_broker import RabbitMQPublisher


class PaymentPublisher(RabbitMQPublisher):
    exchange = Exchanges.payment
