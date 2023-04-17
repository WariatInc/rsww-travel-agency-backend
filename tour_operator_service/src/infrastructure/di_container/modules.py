from src.di_container.injector import Module
from injector import singleton

class InfrastructureModule(Module):
    def configure(self, binder: Binder) -> None:
        self.bind(SessionFactory)

    @provider
    @singleton
    def provide_sqlalchemy_engine(self, config: Config) -> SQLAlchemyEngine:
        return SQLAlchemyEngine(config)
