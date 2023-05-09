from injector import Binder, provider, singleton
from src.di_container.injector import Module
from src.infrastructure.message_broker import RabbitMQConnectionFactory
from src.payment.api import ProcessReservationPaymentResource
from src.payment.domain.commands import ProcessReservationPaymentCommand
from src.payment.domain.ports import (IPaymentUnitOfWork,
                                      IProcessReservationPaymentCommand)
from src.payment.infrastructure.message_broker.producer import PaymentPublisher
from src.payment.infrastructure.storage.unit_of_work import PaymentUnitOfWork


class PaymentModule(Module):
    def configure(self, binder: Binder) -> None:
        # commands
        self.bind(
            IProcessReservationPaymentCommand, ProcessReservationPaymentCommand
        )

        # unit of work
        self.bind(IPaymentUnitOfWork, PaymentUnitOfWork)

        # resources
        self.bind(ProcessReservationPaymentResource)

    @provider
    @singleton
    def provide_payment_publisher(
        self, connection_factory: RabbitMQConnectionFactory
    ) -> PaymentPublisher:
        return PaymentPublisher(connection_factory)
