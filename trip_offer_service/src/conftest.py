import pytest
from pytest_factoryboy import register

from src.app import create_app
from src.config import TestConfig

from src.infrastructure.storage import MongoClient

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
def mongo_client(app: pytest.fixture):
    return MongoClient(app.config)


@pytest.fixture(scope="function")
def db(mongo_client: pytest.fixture):
    db = mongo_client.get_db()
    yield db
    db.example.drop()
