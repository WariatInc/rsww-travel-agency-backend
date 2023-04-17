from typing import TYPE_CHECKING
if TYPE_CHECKING: 
    from src.config import Config
from sqlalchemy import Engine, create_engine
from injector import Injector, inject

class TourOperatorService:
    def apply_config(self, config: "Config") -> None:
        self.config = config

