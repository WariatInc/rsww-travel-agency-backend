from uuid import UUID

from src.consts import ReservationState
from src.reservation_read_store.domain.ports import (
    IReservationReadStoreSynchronizationCommand,
    IReservationReadStoreUnitOfWork,
)


class ReservationReadStoreSynchronizationCommand(
    IReservationReadStoreSynchronizationCommand
):
    def __init__(self, uow: IReservationReadStoreUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, reservation_id: UUID, state: ReservationState) -> None:
        with self._uow:
            self._uow.reservation_read_store_repository.upsert_reservation_read_store(
                reservation_id=reservation_id,
                state=state,
            )
            self._uow.commit()
