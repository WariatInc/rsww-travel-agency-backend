from uuid import UUID

from src.reservation.domain.dtos import ReservationDto
from src.reservation.domain.exceptions import ReservationNotFound
from src.reservation.domain.ports import IGetReservationQuery, IReservationView
from src.user.domain.exceptions import UserNotFoundException
from src.user.domain.ports import IUserView


class GetReservationQuery(IGetReservationQuery):
    def __init__(
        self, reservation_view: IReservationView, user_view: IUserView
    ) -> None:
        self.reservation_view = reservation_view
        self.user_view = user_view

    def get(self, user_gid: UUID, reservation_id: UUID) -> ReservationDto:
        if not (user := self.user_view.get_user_by_gid(user_gid)):
            raise UserNotFoundException

        if not (
            reservation := self.reservation_view.get(user.id, reservation_id)
        ):
            raise ReservationNotFound

        return reservation
