from injector import Injector 
from src.config import Config, DefaultConfig
from src.tour_operator import TourOperatorService
from src.di_container.modules import all_modules, AppModule


def create_app(
    config: Config = DefaultConfig
) -> TourOperatorService:

    app = TourOperatorService()

    configure_app(app, config)
    configure_injector(app)

    return app


def configure_injector(app: TourOperatorService) -> None:
    injector = Injector(auto_bind=False, modules=all_modules)
    injector.binder.install(AppModule(app=app))
    app.set_injector(injector)


def configure_app(app:TourOperatorService, config: Config) -> None:
    app.apply_config(config=config)
