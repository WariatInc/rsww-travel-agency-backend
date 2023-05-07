from uuid import UUID

from src.consts import ReservationState
from src.domain.events import event_factory
from src.reservation.domain.events import ReservationUpdatedEvent
from src.reservation.domain.ports import (
    IReservationUnitOfWork,
    IUpdateReservationCommand,
)
from src.reservation.infrastructure.message_broker.producer import (
    ReservationPublisher,
)


class UpdateReservationCommand(IUpdateReservationCommand):
    def __init__(
        self, uow: IReservationUnitOfWork, publisher: ReservationPublisher
    ) -> None:
        self._uow = uow
        self._publisher = publisher

    def __call__(self, reservation_id: UUID, **update_kwargs) -> None:
        with self._uow:
            reservation = self._uow.reservation_repository.get_reservation(
                reservation_id
            )
            if reservation.state == ReservationState.cancelled:
                update_kwargs.pop("state")

            self._uow.reservation_repository.update_reservation(
                reservation_id, **update_kwargs
            )
            self._uow.commit()

        event = event_factory(
            ReservationUpdatedEvent,
            reservation_id=reservation_id,
            details=update_kwargs,
        )
        self._publisher.publish(event)
