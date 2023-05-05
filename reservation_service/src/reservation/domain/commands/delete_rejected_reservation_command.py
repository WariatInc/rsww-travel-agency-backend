from uuid import UUID

from src.auth.login import current_user
from src.domain.events import event_factory
from src.domain.factories import actor_dto_factory
from src.reservation.domain.events import ReservationDeletedEvent
from src.reservation.domain.exceptions import ReservationNotFound
from src.reservation.domain.ports import (
    IDeleteRejectedReservationCommand,
    IReservationUnitOfWork,
)
from src.reservation.domain.validation import (
    validate_if_reservation_can_be_deleted,
    validate_reservation_ownership,
)
from src.reservation.infrastructure.message_broker.producer import (
    ReservationPublisher,
)


class DeleteRejectedReservationCommand(IDeleteRejectedReservationCommand):
    def __init__(
        self, uow: IReservationUnitOfWork, publisher: ReservationPublisher
    ) -> None:
        self._uow = uow
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
        validate_if_reservation_can_be_deleted(reservation)

        with self._uow:
            self._uow.reservation_repository.delete_reservation(reservation.id)
            self._uow.commit()

        event = event_factory(
            ReservationDeletedEvent, reservation_id=reservation.id
        )
        self._publisher.publish(event)
