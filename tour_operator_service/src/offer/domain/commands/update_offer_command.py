from uuid import UUID

from src.domain.events import event_factory
from src.offer.domain.events import OfferChangedEvent
from src.offer.domain.exceptions import OfferNotFoundException
from src.offer.domain.ports import IOfferUnitOfWork, IUpdateOfferCommand
from src.offer.infrastructure.message_broker.producer import OfferPublisher


class UpdateOfferCommand(IUpdateOfferCommand):
    def __init__(
        self, uow: IOfferUnitOfWork, publisher: OfferPublisher
    ) -> None:
        self._uow = uow
        self._publisher = publisher

    def __call__(self, offer_id: UUID, **update_kwargs) -> None:
        with self._uow:
            if not self._uow.offer_repository.get_offer(offer_id):
                raise OfferNotFoundException

        with self._uow:
            self._uow.offer_repository.update_offer(offer_id, update_kwargs)
            self._uow.commit()

        event = event_factory(
            OfferChangedEvent, offer_id=offer_id, details=update_kwargs
        )
        self._publisher.publish(event)
