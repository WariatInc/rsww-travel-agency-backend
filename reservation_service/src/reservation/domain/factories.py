from typing import TYPE_CHECKING

from src.reservation.domain.dtos import ReservationDto

if TYPE_CHECKING:
    from src.reservation.infrastructure.storage.models import Reservation


def reservation_dto_factory(reservation: "Reservation") -> ReservationDto:
    return ReservationDto(
        id=reservation.id,
        state=reservation.state,
        offer_id=reservation.offer_id,
    )
