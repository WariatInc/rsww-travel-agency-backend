from uuid import UUID

from src.domain.events import event_factory
from src.offer.domain.events import OfferChangedEvent, TourChangedEvent
from src.offer.domain.exceptions import TourNotFoundException
from src.offer.domain.ports import (
    IGetOfferPriceQuery,
    ITourUnitOfWork,
    IUpdateTourCommand,
)
from src.offer.infrastructure.message_broker.producer import OfferPublisher


class UpdateTourCommand(IUpdateTourCommand):
    def __init__(
        self,
        uow: ITourUnitOfWork,
        publisher: OfferPublisher,
        get_offer_price_query: IGetOfferPriceQuery,
    ) -> None:
        self._uow = uow
        self._publisher = publisher
        self._get_offer_price_query = get_offer_price_query

    def __call__(self, tour_id: UUID, **kwargs) -> None:
        with self._uow:
            if not self._uow.tour_repository.get_tour(tour_id):
                raise TourNotFoundException

        with self._uow:
            self._uow.tour_repository.update_tour(tour_id, kwargs)
            self._uow.commit()

        with self._uow:
            offers = self._uow.offer_repository.get_offers_by_tour_id(tour_id)

        self._publisher.publish(
            data=event_factory(
                TourChangedEvent, tour_id=tour_id, details=kwargs
            )
        )

        for offer in offers:
            self._publisher.publish(
                data=event_factory(
                    OfferChangedEvent,
                    offer_id=offer.id,
                    details=dict(
                        price=self._get_offer_price_query.get(offer.id, 0, 0)
                    ),
                )
            )
