from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Event:
    id: UUID
    time: datetime
    type: str


@dataclass
class DomainEvent(Event):
    pass


def event_factory(event_class: type[DomainEvent], **kwargs) -> DomainEvent:
    return event_class(
        id=uuid4(), time=datetime.utcnow(), type=event_class.__name__, **kwargs
    )
