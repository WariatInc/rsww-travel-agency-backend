from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from src.consts import PaymentItem, PaymentState
from src.payment.domain.factories import payment_dto_factory
from src.payment.domain.ports import IPaymentRepository
from src.payment.infrastructure.storage.models import Payment

if TYPE_CHECKING:
    from src.payment.domain.dtos import PaymentDto


class PaymentRepository(IPaymentRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def check_if_item_is_paid(self, item_id: UUID) -> bool:
        return self._session.query(
            self._session.query(Payment)
            .filter(
                Payment.item_id == item_id,
                Payment.state == PaymentState.finalized,
            )
            .exists()
        ).scalar()

    def check_if_item_payment_is_in_pending_state(self, item_id: UUID) -> bool:
        return self._session.query(
            self._session.query(Payment)
            .filter(
                Payment.item_id == item_id,
                Payment.state == PaymentState.pending,
            )
            .exists()
        ).scalar()

    def create_payment(
        self, item_id: UUID, item: "PaymentItem", state: "PaymentState"
    ) -> "PaymentDto":
        payment = Payment(id=uuid4(), item_id=item_id, item=item, state=state)
        self._session.add(payment)

        return payment_dto_factory(payment)

    def update_payment(self, payment_id: UUID, **update_kwargs) -> None:
        self._session.query(Payment).filter(Payment.id == payment_id).update(
            update_kwargs
        )
