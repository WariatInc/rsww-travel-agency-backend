from src.domain.exceptions import DomainException


class ReservationException(DomainException):
    pass


class ReservationExistInPendingAcceptedOrPaidStateException(
    ReservationException
):
    pass


class ReservationNotFound(ReservationException):
    pass


class ReservationAlreadyCancelled(ReservationException):
    pass


class ReservationIsPaid(ReservationException):
    pass


class UserIsNotReservationOwner(ReservationException):
    pass


class ReservationCannotBeDeleted(ReservationException):
    pass
