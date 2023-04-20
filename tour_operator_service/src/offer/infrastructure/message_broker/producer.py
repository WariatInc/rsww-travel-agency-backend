from src.consts import Exchanges
from src.infrastructure.message_broker import RabbitMQPublisher


class OfferPublisher(RabbitMQPublisher):
    exchange = Exchanges.Offer


class ReservationPublisher(RabbitMQPublisher):
    exchange = Exchanges.Reservation
