from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from src.consts import PaymentItem, PaymentState


@dataclass
class PaymentDto:
    id: UUID
    item_id: UUID
    item: "PaymentItem"
    state: "PaymentState"
