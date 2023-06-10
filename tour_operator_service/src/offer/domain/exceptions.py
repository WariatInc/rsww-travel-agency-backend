from src.domain.exceptions import DomainException


class OfferNotFoundException(DomainException):
    pass


class InvalidOfferConfiguration(DomainException):
    pass


class TourNotFoundException(DomainException):
    pass
