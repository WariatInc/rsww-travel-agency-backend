from src.domain.exceptions import DomainException


class OfferException(DomainException):
    pass


class OfferNotFoundException(OfferException):
    pass


class InvalidOfferConfiguration(OfferException):
    pass
