from src.consts import StrEnum, auto


class ERROR(StrEnum):
    reservation_exist_in_pending_or_accepted_state_error = auto()
    reservation_not_found_error = auto()
    reservation_already_cancelled_error = auto()
    actor_is_not_reservation_owner_error = auto()
