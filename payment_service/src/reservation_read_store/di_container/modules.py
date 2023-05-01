from injector import Binder

from src.di_container.injector import Module
from src.reservation_read_store.domain.commands import (
    ReservationReadStoreSynchronizationCommand,
)
from src.reservation_read_store.domain.ports import (
    IReservationReadStoreSynchronizationCommand,
    IReservationReadStoreUnitOfWork,
)
from src.reservation_read_store.infrastructure.storage.unit_of_work import (
    ReservationReadStoreUnitOfWork,
)


class ReservationReadStoreModule(Module):
    def configure(self, binder: Binder) -> None:
        # Commands
        self.bind(
            IReservationReadStoreSynchronizationCommand,
            ReservationReadStoreSynchronizationCommand,
        )

        # Unit of works
        self.bind(
            IReservationReadStoreUnitOfWork, ReservationReadStoreUnitOfWork
        )
