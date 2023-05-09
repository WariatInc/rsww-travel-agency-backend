from uuid import UUID

from src.consts import RejectionReason, ReservationState
from src.domain.events import event_factory
from src.offer.domain.events import ReservationCheckedEvent
from src.offer.domain.ports import (
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
        publisher: ReservationPublisher,
    ) -> None:
        self._uow = uow
        self._update_offer_command = update_offer_command
        self._publisher = publisher

    def __call__(self, offer_id: UUID, reservation_id: UUID) -> None:
        with self._uow:
            can_be_reserved = (
                self._uow.offer_repository.check_if_offer_can_be_reserved(
                    offer_id
                )
            )

        if can_be_reserved:
            self._update_offer_command(offer_id, available=False)
            event = event_factory(
                ReservationCheckedEvent,
                reservation_id=reservation_id,
                reservation_state=ReservationState.accepted,
            )
            self._publisher.publish(event)
        else:
            event = event_factory(
                ReservationCheckedEvent,
                reservation_id=reservation_id,
                reservation_state=ReservationState.rejected,
                reason=RejectionReason.not_available,
            )
            self._publisher.publish(event)
