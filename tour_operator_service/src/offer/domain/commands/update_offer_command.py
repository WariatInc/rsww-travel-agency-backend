from uuid import UUID

from src.domain.events import event_factory
from src.offer.domain.events import OfferChangedEvent
from src.offer.domain.exceptions import OfferNotFoundException
from src.offer.domain.ports import (
    IGetOfferPriceQuery,
    IOfferUnitOfWork,
    IUpdateOfferCommand,
)
from src.offer.infrastructure.message_broker.producer import OfferPublisher


class UpdateOfferCommand(IUpdateOfferCommand):
    def __init__(
        self,
        uow: IOfferUnitOfWork,
        publisher: OfferPublisher,
        get_offer_price_query: IGetOfferPriceQuery,
    ) -> None:
        self._uow = uow
        self._publisher = publisher
        self._get_offer_price_query = get_offer_price_query

    def __call__(self, offer_id: UUID, **update_kwargs) -> None:
        with self._uow:
            if not self._uow.offer_repository.get_offer(offer_id):
                raise OfferNotFoundException

        with self._uow:
            self._uow.offer_repository.update_offer(offer_id, update_kwargs)
            self._uow.commit()

        update_kwargs["price"] = self._get_offer_price_query.get(
            offer_id, 0, 0
        )
        event = event_factory(
            OfferChangedEvent, offer_id=offer_id, details=update_kwargs
        )
        self._publisher.publish(event)
