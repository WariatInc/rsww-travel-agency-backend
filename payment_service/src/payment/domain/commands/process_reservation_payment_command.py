from random import uniform
from time import sleep
from uuid import UUID

from src.consts import PaymentItem, PaymentState, ReservationState
from src.domain.events import event_factory
from src.payment.domain.events import ItemPaidEvent
from src.payment.domain.exceptions import (ItemAlreadyPaid, ItemCannotBePaid,
                                           ItemNotFound, ItemPaymentInProgress)
from src.payment.domain.ports import (IPaymentUnitOfWork,
                                      IProcessReservationPaymentCommand)
from src.payment.infrastructure.message_broker.producer import PaymentPublisher
from src.reservation_read_store.domain.ports import IReservationReadStoreView


class ProcessReservationPaymentCommand(IProcessReservationPaymentCommand):
    def __init__(
        self,
        uow: IPaymentUnitOfWork,
        reservation_read_store_view: IReservationReadStoreView,
        publisher: PaymentPublisher,
    ) -> None:
        self._uow = uow
        self._reservation_read_store_view = reservation_read_store_view
        self._publisher = publisher

    @staticmethod
    def _process_payment() -> bool:
        sleep(5)
        return uniform(0, 1) > 0.3

    def __call__(self, item_id: UUID) -> PaymentState:
        if not (
            item := self._reservation_read_store_view.get_reservation(item_id)
        ):
            raise ItemNotFound

        with self._uow:
            if self._uow.payment_repository.check_if_item_is_paid(
                item.reservation_id
            ):
                raise ItemAlreadyPaid
            if self._uow.payment_repository.check_if_item_payment_is_in_pending_state(
                item.reservation_id
            ):
                raise ItemPaymentInProgress

        if item.state != ReservationState.accepted:
            raise ItemCannotBePaid

        with self._uow:
            payment = self._uow.payment_repository.create_payment(
                item_id=item_id,
                item=PaymentItem.reservation,
                state=PaymentState.pending,
            )
            self._uow.commit()

        if self._process_payment():
            with self._uow:
                self._uow.payment_repository.update_payment(
                    payment.id, state=PaymentState.finalized
                )
                self._uow.commit()
            event = event_factory(
                ItemPaidEvent, item_id=payment.item_id, item_type=payment.item
            )
            self._publisher.publish(event)

            return PaymentState.finalized

        with self._uow:
            self._uow.payment_repository.update_payment(
                payment.id, state=PaymentState.rejected
            )
            self._uow.commit()

        return PaymentState.rejected
