from src.consts import CancelReason
from src.reservation.domain.ports import (
    ICancelReservationCommand,
    IReservationsToCancelView,
)


def cancel_accepted_reservations_after_timeout(
    reservations_to_cancel_view: IReservationsToCancelView,
    cancel_reservation_command: ICancelReservationCommand,
) -> None:
    reservations = reservations_to_cancel_view.get()
    for reservation in reservations:
        cancel_reservation_command(
            reservation.user.gid,
            reservation.id,
            cancel_reason=CancelReason.payment_timeout,
        )
