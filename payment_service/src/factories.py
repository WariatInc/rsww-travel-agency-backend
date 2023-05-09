from inspect import isclass
from typing import Any

from factory import Factory
from factory.alchemy import SQLAlchemyModelFactory
from src.extensions import db


def is_factory(obj: Any) -> bool:
    return isclass(obj) and issubclass(obj, Factory) and not obj._meta.abstract


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
