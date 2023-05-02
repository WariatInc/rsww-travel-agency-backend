from src.enum import StrEnum, auto


class ERROR(StrEnum):
    item_already_paid = auto()
    item_cannot_be_paid = auto()
    item_not_found = auto()
    item_payment_in_progress = auto()
