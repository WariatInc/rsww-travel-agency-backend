from src.consts import ReservationState
from src.domain.dtos import ActorDto
from src.reservation.domain.dtos import ReservationDto
from src.reservation.domain.exceptions import (
    ActorIsNotReservationOwner,
    ReservationAlreadyCancelled,
)


def validate_reservation_ownership(
    actor: ActorDto, reservation: ReservationDto
) -> None:
    if actor.id != reservation.user_id:
        raise ActorIsNotReservationOwner


def validate_if_reservation_can_be_cancelled(
    reservation: ReservationDto,
) -> None:
    if reservation.state in [
        ReservationState.cancelled,
        ReservationState.rejected,
    ]:
        raise ReservationAlreadyCancelled
