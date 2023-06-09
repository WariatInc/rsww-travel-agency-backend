from typing import TYPE_CHECKING

from src.reservation.domain.dtos import (
    ReservationDetailsDto,
    ReservationDto,
    ReservationEventDashboardDto,
)
from src.user.domain.factories import user_dto_factory

if TYPE_CHECKING:
    from src.reservation.infrastructure.storage.models import (
        Reservation,
        ReservationEventDashboard,
    )


def reservation_dto_factory(reservation: "Reservation") -> ReservationDto:
    return ReservationDto(
        id=reservation.id,
        state=reservation.state,
        offer_id=reservation.offer_id,
        user=user_dto_factory(reservation.user) if reservation.user else None,
        rejection_reason=reservation.rejection_reason,
        price=reservation.price,
    )


def reservation_details_dto_factory(
    reservation: "Reservation",
) -> ReservationDetailsDto:
    return ReservationDetailsDto(
        id=reservation.id,
        state=reservation.state,
        offer_id=reservation.offer_id,
        user=user_dto_factory(reservation.user) if reservation.user else None,
        rejection_reason=reservation.rejection_reason,
        kids_up_to_3=reservation.kids_up_to_3,
        kids_up_to_10=reservation.kids_up_to_10,
        price=reservation.price,
    )


def reservation_event_dashboard_dto_factory(
    reservation_event_dashboard: "ReservationEventDashboard",
) -> ReservationEventDashboardDto:
    return ReservationEventDashboardDto(
        id=reservation_event_dashboard.id,
        offer_id=reservation_event_dashboard.offer_id,
        reservation_id=reservation_event_dashboard.reservation_id,
        state=reservation_event_dashboard.state,
        timestamp=reservation_event_dashboard.timestamp,
    )
