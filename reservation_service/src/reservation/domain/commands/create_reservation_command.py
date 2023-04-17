from uuid import UUID

from src.reservation.domain.ports import (
    ICreateReservationCommand,
    IReservationUnitOfWork,
)


class CreateReservationCommand(ICreateReservationCommand):
    def __init__(self, uow: IReservationUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, user_id: UUID, offer_id: UUID) -> None:
        with self._uow:
            if self._uow.reservation_repository.check_if_offer_reservation_exits_in_pending_or_accepted_state(
                user_id, offer_id
            ):
                raise
            self._uow.reservation_repository.create_reservation(
                user_id, offer_id
            )
            self._uow.commit()
