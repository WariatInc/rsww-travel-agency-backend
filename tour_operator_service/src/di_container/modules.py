from injector import Binder, singleton

from src.config import Config
from src.di_container.injector import Module
from src.infrastructure.di_container.modules import InfrastructureModule
from src.offer.di_container.modules import OfferModule
from src.tour_operator import TourOperatorService

all_modules = [InfrastructureModule, OfferModule]


class AppModule(Module):
    def __init__(self, app: TourOperatorService):
        self.app = app

    def configure(self, binder: Binder) -> None:
        binder.bind(TourOperatorService, to=self.app, scope=singleton)
        binder.bind(Config, to=self.app.config, scope=singleton)
