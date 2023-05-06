from src.consts import StrEnum, auto


class ERROR(StrEnum):
    reservation_exist_in_pending_accepted_or_paid_state_error = auto()
    reservation_not_found_error = auto()
    reservation_already_cancelled_error = auto()
    actor_is_not_reservation_owner_error = auto()
    reservation_is_paid_cannot_be_cancelled = auto()
    reservation_cannot_be_deleted = auto()
