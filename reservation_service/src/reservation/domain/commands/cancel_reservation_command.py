from uuid import UUID

from src.auth.login import current_user
from src.consts import ReservationState
from src.domain.events import event_factory
from src.domain.factories import actor_dto_factory
from src.reservation.domain.events import ReservationCancelledEvent
from src.reservation.domain.exceptions import ReservationNotFound
from src.reservation.domain.ports import (
    ICancelReservationCommand,
    IReservationUnitOfWork,
    IUpdateReservationCommand,
)
from src.reservation.domain.validation import (
    validate_if_reservation_can_be_cancelled,
    validate_reservation_ownership,
)
from src.reservation.infrastructure.message_broker.producer import (
    ReservationPublisher,
)


class CancelReservationCommand(ICancelReservationCommand):
    def __init__(
        self,
        uow: IReservationUnitOfWork,
        update_reservation_command: IUpdateReservationCommand,
        publisher: ReservationPublisher,
    ) -> None:
        self._uow = uow
        self._update_reservation_command = update_reservation_command
        self._publisher = publisher

    def __call__(self, reservation_id: UUID) -> None:
        actor = actor_dto_factory(current_user)

        with self._uow:
            reservation = self._uow.reservation_repository.get_reservation(
                reservation_id
            )

        if not reservation:
            raise ReservationNotFound

        validate_reservation_ownership(actor=actor, reservation=reservation)
        validate_if_reservation_can_be_cancelled(reservation)

        self._update_reservation_command(
            reservation_id=reservation.id, state=ReservationState.cancelled
        )

        event = event_factory(
            ReservationCancelledEvent, offer_id=reservation.offer_id
        )
        self._publisher.publish(event)
