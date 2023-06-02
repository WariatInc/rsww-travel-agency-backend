from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import Config


class SQLAlchemyEngine:
    def __init__(self, config: Config) -> None:
        self.engine = create_engine(
            config.SQLALCHEMY_DATABASE_URI,
            pool_pre_ping=True,
            max_overflow=2,
            pool_recycle=300,
            pool_use_lifo=True,
            connect_args=config.SQLALCHEMY_CONNECTION_OPTIONS
        )

    def __call__(self, *args, **kwargs) -> Engine:
        return self.engine


class SessionFactory:
    def __init__(self, sqlalchemy_engine: SQLAlchemyEngine) -> None:
        self._sqlalchemy_engine = sqlalchemy_engine

    def create_session(self) -> Session:
        return sessionmaker(bind=self._sqlalchemy_engine())()
