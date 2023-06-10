import logging
from typing import TYPE_CHECKING

from src.offer.domain.ports import (
    IRandomizeOfferCommand,
    IRandomizeTourCommand,
)

if TYPE_CHECKING:
    from src.config import Config

import random as rd

from injector import Injector

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(asctime)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("TourOperator")


class TourOperatorService:
    config: "Config"
    injector: Injector

    def apply_config(self, config: "Config") -> None:
        self.config = config

    def set_injector(self, injector: Injector) -> None:
        self.injector = injector

    def run(self) -> None:
        logger.info("Started")
        randomize_offer_command = self.injector.get(IRandomizeOfferCommand)
        randomize_tour_command = self.injector.get(IRandomizeTourCommand)

        while True:
            if rd.uniform(0, 100000) < 0.01:
                randomize_offer_command()
            elif rd.uniform(0, 300000) < 0.01:
                randomize_tour_command()
