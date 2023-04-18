from src.di_container.injector import Module
from injector import singleton, Binder, provider
from src.config import Config
from src.infrastructure.storage import SQLAlchemyEngine, SessionFactory

class InfrastructureModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(SessionFactory)

    @provider
    @singleton
    def provide_sqlalchemy_engine(self, config: Config) -> SQLAlchemyEngine:
        return SQLAlchemyEngine(config)
