from typing import TYPE_CHECKING
from uuid import UUID

from src.domain.events import event_factory
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
from src.user.domain.exceptions import UserNotFoundException

if TYPE_CHECKING:
    from src.reservation.domain.dtos import ReservationDetailsDto


class CreateReservationCommand(ICreateReservationCommand):
    def __init__(
        self, uow: IReservationUnitOfWork, publisher: ReservationPublisher
    ) -> None:
        self._uow = uow
        self._publisher = publisher

    def __call__(
        self,
        user_gid: UUID,
        offer_id: UUID,
        kids_up_to_3: int,
        kids_up_to_10: int,
    ) -> "ReservationDetailsDto":
        with self._uow:
            if not (
                user := self._uow.user_repository.get_user_by_gid(user_gid)
            ):
                raise UserNotFoundException

            if self._uow.reservation_repository.check_if_offer_reservation_exits_in_pending_accepted_or_paid_state(
                offer_id
            ):
                raise ReservationExistInPendingAcceptedOrPaidStateException

            reservation = self._uow.reservation_repository.create_reservation(
                user_id=user.id,
                offer_id=offer_id,
                kids_up_to_3=kids_up_to_3,
                kids_up_to_10=kids_up_to_10,
            )
            self._uow.commit()

        event = event_factory(
            ReservationCreatedEvent,
            offer_id=reservation.offer_id,
            reservation_id=reservation.id,
            kids_up_to_3=reservation.kids_up_to_3,
            kids_up_to_10=reservation.kids_up_to_10,
        )
        self._publisher.publish(event)

        return reservation
