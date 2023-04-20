from src.domain.exceptions import DomainException


class ReservationException(DomainException):
    pass


class ReservationExistInPendingOrAcceptedStateException(ReservationException):
    pass


class ReservationNotFound(ReservationException):
    pass


class ReservationAlreadyCancelled(ReservationException):
    pass


class ActorIsNotReservationOwner(ReservationException):
    pass
