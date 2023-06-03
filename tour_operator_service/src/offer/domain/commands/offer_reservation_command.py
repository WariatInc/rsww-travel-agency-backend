from uuid import UUID

from src.consts import RejectionReason, ReservationState
from src.domain.events import event_factory
from src.offer.domain.events import ReservationCheckedEvent
from src.offer.domain.exceptions import (
    InvalidOfferConfiguration,
    OfferNotFoundException,
)
from src.offer.domain.ports import (
    IGetOfferPriceQuery,
    IOfferReservationCommand,
    IOfferUnitOfWork,
    IUpdateOfferCommand,
)
from src.offer.infrastructure.message_broker.producer import (
    ReservationPublisher,
)


class OfferReservationCommand(IOfferReservationCommand):
    def __init__(
        self,
        uow: IOfferUnitOfWork,
        update_offer_command: IUpdateOfferCommand,
        get_offer_price_query: IGetOfferPriceQuery,
        publisher: ReservationPublisher,
    ) -> None:
        self._uow = uow
        self._update_offer_command = update_offer_command
        self._get_offer_price_query = get_offer_price_query
        self._publisher = publisher

    def __call__(
        self,
        offer_id: UUID,
        reservation_id: UUID,
        kids_up_to_3: int,
        kids_up_to_10: int,
    ) -> None:
        with self._uow:
            can_be_reserved = (
                self._uow.offer_repository.check_if_offer_can_be_reserved(
                    offer_id
                )
            )

        if can_be_reserved:
            try:
                price = self._get_offer_price_query.get(
                    offer_id, kids_up_to_3, kids_up_to_10
                )

                self._update_offer_command(offer_id, available=False)
                event = event_factory(
                    ReservationCheckedEvent,
                    reservation_id=reservation_id,
                    reservation_state=ReservationState.accepted,
                    price=price,
                )
            except InvalidOfferConfiguration:
                event = event_factory(
                    ReservationCheckedEvent,
                    reservation_id=reservation_id,
                    reservation_state=ReservationState.rejected,
                    reason=RejectionReason.invalid_offer_configuration,
                )
            except OfferNotFoundException:
                event = event_factory(
                    ReservationCheckedEvent,
                    reservation_id=reservation_id,
                    reservation_state=ReservationState.rejected,
                    reason=RejectionReason.offer_not_found,
                )
        else:
            event = event_factory(
                ReservationCheckedEvent,
                reservation_id=reservation_id,
                reservation_state=ReservationState.rejected,
                reason=RejectionReason.not_available,
            )

        self._publisher.publish(event)
