from typing import TYPE_CHECKING

from src.reservation_read_store.domain.dtos import ReservationDto

if TYPE_CHECKING:
    from src.reservation_read_store.infrastructure.storage.models import (
        ReservationReadStore,
    )


def reservation_dto_factory(
    reservation: "ReservationReadStore",
) -> ReservationDto:
    return ReservationDto(
        reservation_id=reservation.reservation_id, state=reservation.state
    )
