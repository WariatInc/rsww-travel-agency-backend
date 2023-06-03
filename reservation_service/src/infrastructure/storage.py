from flask import Config
from sqlalchemy import Engine, NullPool, create_engine
from sqlalchemy.orm import Session, sessionmaker


class SQLAlchemyEngine:
    def __init__(self, config: Config) -> None:
        self.engine = create_engine(
            config["SQLALCHEMY_DATABASE_URI"],
            pool_pre_ping=True,
            max_overflow=2,
            pool_recycle=300,
            pool_use_lifo=True,
            connect_args=config["SQLALCHEMY_CONNECTION_OPTIONS"],
        )

    def __call__(self, *args, **kwargs) -> Engine:
        return self.engine


class SQLAlchemyReadOnlyEngine:
    def __init__(self, config: Config) -> None:
        self.engine = create_engine(
            config["SQLALCHEMY_BINDS"]["readonly"],
            poolclass=NullPool,
            pool_pre_ping=True,
            connect_args=config["SQLALCHEMY_CONNECTION_OPTIONS"],
        )

    def __call__(self, *args, **kwargs) -> Engine:
        return self.engine


class SessionFactory:
    def __init__(self, sqlalchemy_engine: SQLAlchemyEngine) -> None:
        self._sqlalchemy_engine = sqlalchemy_engine

    def create_session(self) -> Session:
        return sessionmaker(bind=self._sqlalchemy_engine())()


class ReadOnlySessionFactory:
    def __init__(
        self, sqlalchemy_read_only_engine: SQLAlchemyReadOnlyEngine
    ) -> None:
        self._sqlalchemy_read_only_engine = sqlalchemy_read_only_engine

    def create_session(self) -> Session:
        return sessionmaker(bind=self._sqlalchemy_read_only_engine())()
