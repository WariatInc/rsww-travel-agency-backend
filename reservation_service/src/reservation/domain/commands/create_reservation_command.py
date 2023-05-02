from uuid import UUID

from src.auth.login import current_user
from src.domain.events import event_factory
from src.domain.factories import actor_dto_factory
from src.reservation.domain.events import ReservationCreatedEvent
from src.reservation.domain.exceptions import (
    ReservationExistInPendingAcceptedOrPaidStateException,
)
from src.reservation.domain.ports import (
    ICreateReservationCommand,
    IReservationUnitOfWork,
)
from src.reservation.infrastructure.message_broker.producer import (
    ReservationPublisher,
)


class CreateReservationCommand(ICreateReservationCommand):
    def __init__(
        self, uow: IReservationUnitOfWork, publisher: ReservationPublisher
    ) -> None:
        self._uow = uow
        self._publisher = publisher

    def __call__(self, offer_id: UUID) -> None:
        actor = actor_dto_factory(current_user)

        with self._uow:
            if self._uow.reservation_repository.check_if_offer_reservation_exits_in_pending_accepted_or_paid_state(
                offer_id
            ):
                raise ReservationExistInPendingAcceptedOrPaidStateException

            reservation = self._uow.reservation_repository.create_reservation(
                user_id=actor.id, offer_id=offer_id
            )
            self._uow.commit()

        event = event_factory(
            ReservationCreatedEvent,
            offer_id=reservation.offer_id,
            reservation_id=reservation.id,
        )
        self._publisher.publish(event)
