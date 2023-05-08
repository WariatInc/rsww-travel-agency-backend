from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.events import Event


@dataclass
class ItemPaidEvent(Event):
    item_id: UUID
    item_type: str

    @classmethod
    def from_rabbitmq_message(cls, message: dict[str, str]) -> "ItemPaidEvent":
        return cls(
            id=UUID(message.get("id")),
            time=datetime.fromisoformat(message.get("time")),
            type=message.get("type"),
            item_id=UUID(message.get("item_id")),
            item_type=message.get("item_type"),
        )
