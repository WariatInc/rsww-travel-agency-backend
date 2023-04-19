from src.auth.login import current_user
from src.domain.factories import actor_dto_factory
from src.reservation.domain.dtos import ReservationDto
from src.reservation.domain.ports import (
    IGetUserReservationsQuery,
    IReservationListView,
)


class GetUserReservationQuery(IGetUserReservationsQuery):
    def __init__(self, reservation_list_view: IReservationListView) -> None:
        self.reservation_list_view = reservation_list_view

    def get(self) -> list[ReservationDto]:
        actor = actor_dto_factory(current_user)
        return self.reservation_list_view.get_list(actor.id)
