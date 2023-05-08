from uuid import UUID

from src.reservation_read_store.domain.ports import (
    IDeleteReservationFromReadStoreCommand,
    IReservationReadStoreUnitOfWork,
)


class DeleteReservationFromReadStoreCommand(
    IDeleteReservationFromReadStoreCommand
):
    def __init__(self, uow: IReservationReadStoreUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, reservation_id: UUID) -> None:
        with self._uow:
            self._uow.reservation_read_store_repository.delete_reservation_from_read_store(
                reservation_id
            )
            self._uow.commit()
