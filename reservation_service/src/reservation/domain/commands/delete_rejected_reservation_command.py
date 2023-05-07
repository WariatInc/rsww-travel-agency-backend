from uuid import UUID

from src.domain.events import event_factory
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
from src.user.domain.exceptions import UserNotFoundException


class DeleteRejectedReservationCommand(IDeleteRejectedReservationCommand):
    def __init__(
        self, uow: IReservationUnitOfWork, publisher: ReservationPublisher
    ) -> None:
        self._uow = uow
        self._publisher = publisher

    def __call__(self, user_gid: UUID, reservation_id: UUID) -> None:
        with self._uow:
            user = self._uow.user_repository.get_user_by_gid(user_gid)
            reservation = self._uow.reservation_repository.get_reservation(
                reservation_id
            )

        if not user:
            raise UserNotFoundException

        if not reservation:
            raise ReservationNotFound

        validate_reservation_ownership(user=user, reservation=reservation)
        validate_if_reservation_can_be_deleted(reservation)

        with self._uow:
            self._uow.reservation_repository.delete_reservation(reservation.id)
            self._uow.commit()

        event = event_factory(
            ReservationDeletedEvent, reservation_id=reservation.id
        )
        self._publisher.publish(event)
