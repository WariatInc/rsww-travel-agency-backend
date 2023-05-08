from uuid import UUID

from src.reservation.domain.dtos import ReservationDto
from src.reservation.domain.ports import (
    IGetUserReservationsQuery,
    IReservationListView,
)
from src.user.domain.exceptions import UserNotFoundException
from src.user.domain.ports import IUserView


class GetUserReservationsQuery(IGetUserReservationsQuery):
    def __init__(
        self, reservation_list_view: IReservationListView, user_view: IUserView
    ) -> None:
        self.reservation_list_view = reservation_list_view
        self.user_view = user_view

    def get(self, user_gid: UUID) -> list[ReservationDto]:
        if not (user := self.user_view.get_user_by_gid(user_gid)):
            raise UserNotFoundException

        return self.reservation_list_view.get_list(user.id)
