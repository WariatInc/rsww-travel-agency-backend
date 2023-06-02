from src.reservation.domain.ports import IUpdateReservationEventDashboardCommand, IReservationEventDashboardUnitOfWork
from uuid import UUID
from datetime import datetime


class UpdateReservationEventDashboardCommand(IUpdateReservationEventDashboardCommand):
    def __init__(self, uow: IReservationEventDashboardUnitOfWork) -> None:
        self._uow = uow

    def __call__(self, reservation_event_id: UUID, reservation_id: UUID, timestamp: datetime) -> None:
        with self._uow:
            reservation = self._uow.reservation_repository.get_reservation(reservation_id)
            self._uow.reservation_event_dashboard_repository.add_reservation_event(
                reservation_event_id=reservation_event_id,
                timestamp=timestamp,
                reservation_dto=reservation
            )
