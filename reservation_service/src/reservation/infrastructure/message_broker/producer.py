from src.consts import Exchanges
from src.infrastructure.message_broker import RabbitMQPublisher


class ReservationPublisher(RabbitMQPublisher):
    exchange = Exchanges.Reservation
