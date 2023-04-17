from uuid import UUID

from src.reservation.domain.ports import (
    ICancelReservationCommand,
    IReservationUnitOfWork,
)


class CancelReservationCommand(ICancelReservationCommand):
    def __init__(self, uow: IReservationUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, offer_id: UUID) -> None:
        pass
