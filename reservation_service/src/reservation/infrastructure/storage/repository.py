from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Session

from src.consts import ReservationState
from src.reservation.domain.dtos import ReservationDetailsDto, ReservationDto
from src.reservation.domain.factories import reservation_details_dto_factory
from src.reservation.domain.ports import IReservationRepository, IReservationEventDashboardRepository
from src.reservation.infrastructure.storage.models import Reservation, ReservationEventDashboard


class ReservationRepository(IReservationRepository):
    def __init__(self, session: Session):
        self._session = session

    def create_reservation(
        self,
        user_id: UUID,
        offer_id: UUID,
        kids_up_to_3: int,
        kids_up_to_10: int,
    ) -> ReservationDetailsDto:
        reservation = Reservation(
            id=uuid4(),
            user_id=user_id,
            offer_id=offer_id,
            kids_up_to_3=kids_up_to_3,
            kids_up_to_10=kids_up_to_10,
        )
        self._session.add(reservation)
        return reservation_details_dto_factory(reservation)

    def update_reservation(
        self, reservation_id: UUID, **update_kwargs
    ) -> None:
        self._session.query(Reservation).filter(
            Reservation.id == reservation_id
        ).update(update_kwargs)

    def delete_reservation(self, reservation_id: UUID) -> None:
        self._session.query(Reservation).filter(
            Reservation.id == reservation_id
        ).delete()

    def get_reservation(
        self, reservation_id: UUID
    ) -> Optional[ReservationDetailsDto]:
        if (
            reservation := self._session.query(Reservation)
            .filter(Reservation.id == reservation_id)
            .one_or_none()
        ):
            return reservation_details_dto_factory(reservation)

    def check_if_offer_reservation_exits_in_pending_accepted_or_paid_state(
        self, offer_id: UUID
    ) -> bool:
        return self._session.query(
            self._session.query(Reservation)
            .filter(
                Reservation.offer_id == offer_id,
                Reservation.state.in_(
                    [
                        ReservationState.pending,
                        ReservationState.accepted,
                        ReservationState.paid,
                    ]
                ),
            )
            .exists()
        ).scalar()


class ReservationEventDashboardRepository(IReservationEventDashboardRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_reservation_event(self, reservation_event_id: UUID, timestamp: datetime, reservation_dto: ReservationDto) -> None:
        self._session.add(
            ReservationEventDashboard(
                id=reservation_event_id,
                reservation_id=reservation_dto.id,
                offer_id=reservation_dto.offer_id,
                state=reservation_dto.state,
                timestamp=timestamp
            )
        )
