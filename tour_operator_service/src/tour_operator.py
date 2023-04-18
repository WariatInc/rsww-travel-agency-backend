from typing import TYPE_CHECKING
if TYPE_CHECKING: 
    from src.config import Config
from injector import Injector, inject
from src.infrastructure.storage import SessionFactory


class TourOperatorService:
    def apply_config(self, config: "Config") -> None:
        self.config = config

    def set_injector(self, injector: Injector) -> None:
        self.injector = injector

    def run(self) -> None:
        session_factory = self.injector.get(SessionFactory)
