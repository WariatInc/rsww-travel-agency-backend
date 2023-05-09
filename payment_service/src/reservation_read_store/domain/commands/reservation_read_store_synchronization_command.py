from uuid import UUID

from src.reservation_read_store.domain.ports import (
    IReservationReadStoreSynchronizationCommand,
    IReservationReadStoreUnitOfWork)


class ReservationReadStoreSynchronizationCommand(
    IReservationReadStoreSynchronizationCommand
):
    def __init__(self, uow: IReservationReadStoreUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, reservation_id: UUID, **upsert_kwargs) -> None:
        with self._uow:
            self._uow.reservation_read_store_repository.upsert_reservation_read_store(
                reservation_id=reservation_id, **upsert_kwargs
            )
            self._uow.commit()
