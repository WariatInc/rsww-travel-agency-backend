from uuid import UUID

from src.reservation.domain.ports import (
    IReservationUnitOfWork,
    IUpdateReservationCommand,
)


class UpdateReservationCommand(IUpdateReservationCommand):
    def __init__(self, uow: IReservationUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, reservation_id: UUID, **update_kwargs) -> None:
        with self._uow:
            self._uow.reservation_repository.update_reservation(
                reservation_id, **update_kwargs
            )
            self._uow.commit()
