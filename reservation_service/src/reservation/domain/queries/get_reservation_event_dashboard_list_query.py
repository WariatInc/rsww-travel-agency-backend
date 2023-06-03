from src.reservation.domain.dtos import ReservationEventDashboardDto
from src.reservation.domain.ports import (
    IGetReservationEventDashboardListQuery,
    IReservationEventDashboardListView,
)


class GetReservationEventDashboardListQuery(
    IGetReservationEventDashboardListQuery
):
    def __init__(
        self,
        reservation_event_dashboard_list_view: IReservationEventDashboardListView,
    ) -> None:
        self._reservation_event_dashboard_list_view = (
            reservation_event_dashboard_list_view
        )

    def get(
        self, page: int, size: int
    ) -> tuple[list[ReservationEventDashboardDto], int]:
        return self._reservation_event_dashboard_list_view.get_list(page, size)
