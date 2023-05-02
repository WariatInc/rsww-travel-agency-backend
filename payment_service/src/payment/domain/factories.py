from typing import TYPE_CHECKING

from src.payment.domain.dtos import PaymentDto

if TYPE_CHECKING:
    from src.payment.infrastructure.storage.models import Payment


def payment_dto_factory(payment: "Payment") -> PaymentDto:
    return PaymentDto(
        id=payment.id,
        item_id=payment.item_id,
        item=payment.item,
        state=payment.state,
    )
