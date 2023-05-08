from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.config import Config

from injector import Injector


class TourOperatorService:
    config: "Config"
    injector: Injector

    def apply_config(self, config: "Config") -> None:
        self.config = config

    def set_injector(self, injector: Injector) -> None:
        self.injector = injector

    @staticmethod
    def run() -> None:
        print("Started")
        while True:
            pass
