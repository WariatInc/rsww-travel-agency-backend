from src.consts import ReservationState
from src.reservation.domain.dtos import ReservationDto
from src.reservation.domain.exceptions import (
    ReservationAlreadyCancelled,
    ReservationCannotBeDeleted,
    ReservationIsPaid,
    UserIsNotReservationOwner,
)
from src.user.domain.dtos import UserDto


def validate_reservation_ownership(
    user: UserDto, reservation: ReservationDto
) -> None:
    if user.id != reservation.user.id:
        raise UserIsNotReservationOwner


def validate_if_reservation_can_be_cancelled(
    reservation: ReservationDto,
) -> None:
    if reservation.state in [
        ReservationState.cancelled,
        ReservationState.rejected,
    ]:
        raise ReservationAlreadyCancelled

    if reservation.state == ReservationState.paid:
        raise ReservationIsPaid


def validate_if_reservation_can_be_deleted(
    reservation: ReservationDto,
) -> None:
    if reservation.state != ReservationState.rejected:
        raise ReservationCannotBeDeleted
