import pytest
from pytest_factoryboy import register
from sqlalchemy.orm import Session

from src.app import create_app
from src.config import TestConfig
from src.extensions import db as _db

from . import factories as ft

for factory_name in dir(ft):
    factory = getattr(ft, factory_name)
    if ft.is_factory(factory):
        register(factory)


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig.PROJECT, TestConfig())
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture(scope="session")
def db_(app: pytest.fixture):
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope="function")
def session(db_: pytest.fixture) -> Session:
    connection = db_.engine.connect()
    transaction = connection.begin()

    yield db_.session

    db_.session.remove()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def session_factory(session: pytest.fixture):
    class TestSessionFactory:
        @classmethod
        def create_session(cls) -> Session:
            return session

    return TestSessionFactory
