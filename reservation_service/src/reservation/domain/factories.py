from typing import TYPE_CHECKING

from src.reservation.domain.dtos import ReservationDetailsDto, ReservationDto

if TYPE_CHECKING:
    from src.reservation.infrastructure.storage.models import Reservation


def reservation_dto_factory(reservation: "Reservation") -> ReservationDto:
    return ReservationDto(
        id=reservation.id,
        state=reservation.state,
        offer_id=reservation.offer_id,
        user_id=reservation.user_id,
        rejection_reason=reservation.rejection_reason,
    )


def reservation_details_dto_factory(
    reservation: "Reservation",
) -> ReservationDetailsDto:
    return ReservationDetailsDto(
        id=reservation.id,
        state=reservation.state,
        offer_id=reservation.offer_id,
        user_id=reservation.user_id,
        rejection_reason=reservation.rejection_reason,
        kids_up_to_3=reservation.kids_up_to_3,
        kids_up_to_10=reservation.kids_up_to_10,
        price=reservation.price,
    )
