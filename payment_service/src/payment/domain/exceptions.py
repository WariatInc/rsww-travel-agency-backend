from src.domain.exceptions import DomainException


class ItemNotFound(DomainException):
    pass


class ItemCannotBePaid(DomainException):
    pass


class ItemAlreadyPaid(DomainException):
    pass


class ItemPaymentInProgress(DomainException):
    pass
