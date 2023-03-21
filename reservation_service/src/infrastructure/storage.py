from flask import Config
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class SQLAlchemyEngine:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.engine = create_engine(config["SQLALCHEMY_DATABASE_URI"])

    def __call__(self, *args, **kwargs) -> Engine:
        return self.engine


class SqlAlchemyReadOnlyEngine:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.engine = create_engine(config["SQLALCHEMY_BINDS"]["readonly"])

    def __call__(self, *args, **kwargs) -> Engine:
        return self.engine


class SessionFactory:
    def __init__(self, sqlalchemy_engine: SQLAlchemyEngine) -> None:
        self._sqlalchemy_engine = sqlalchemy_engine

    def create_session(self) -> Session:
        return sessionmaker(bind=self._sqlalchemy_engine())()


class ReadOnlySessionFactory:
    def __init__(
        self, sqlalchemy_read_only_engine: SqlAlchemyReadOnlyEngine
    ) -> None:
        self._sqlalchemy_read_only_engine = sqlalchemy_read_only_engine

    def create_session(self) -> Session:
        return sessionmaker(bind=self._sqlalchemy_read_only_engine())()
