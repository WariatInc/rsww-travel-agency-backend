from src.enum import StrEnum, auto


class ERROR(StrEnum):
    unauthorized = auto()
    user_wrong_credentials = auto()
