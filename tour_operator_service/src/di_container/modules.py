from src.di_container.injector import Module
from src.infrastructure.di_container.modules import InfrastructureModule
from src.tour_operator import TourOperatorService
from injector import singleton, Binder
from src.config import Config

all_modules = [InfrastructureModule]

class AppModule(Module):
    def __init__(self, app: TourOperatorService):
        self.app = app
        
    def configure(self, binder: Binder) -> None:
        binder.bind(TourOperatorService, to=self.app, scope=singleton)
        binder.bind(Config, to=self.app.config, scope=singleton)
