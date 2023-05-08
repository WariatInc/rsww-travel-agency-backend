from src.consts import Exchanges
from src.infrastructure.message_broker import RabbitMQPublisher


class OfferPublisher(RabbitMQPublisher):
    exchange = Exchanges.offer


class ReservationPublisher(RabbitMQPublisher):
    exchange = Exchanges.reservation
