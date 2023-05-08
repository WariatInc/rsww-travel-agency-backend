from dataclasses import dataclass
from uuid import UUID

from src.consts import PaymentItem
from src.domain.events import DomainEvent


@dataclass
class ItemPaidEvent(DomainEvent):
    item_id: UUID
    item_type: PaymentItem
