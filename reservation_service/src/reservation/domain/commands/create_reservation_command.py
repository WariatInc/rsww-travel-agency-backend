from uuid import UUID

from src.auth.login import current_user
from src.domain.factories import actor_dto_factory
from src.reservation.domain.exceptions import (
    ReservationExistInPendingOrAcceptedStateException,
)
from src.reservation.domain.ports import (
    ICreateReservationCommand,
    IReservationUnitOfWork,
)


class CreateReservationCommand(ICreateReservationCommand):
    def __init__(self, uow: IReservationUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, offer_id: UUID) -> None:
        actor = actor_dto_factory(current_user)

        with self._uow:
            if self._uow.reservation_repository.check_if_offer_reservation_exits_in_pending_or_accepted_state(
                offer_id
            ):
                raise ReservationExistInPendingOrAcceptedStateException

            self._uow.reservation_repository.create_reservation(
                user_id=actor.id, offer_id=offer_id
            )
            self._uow.commit()
