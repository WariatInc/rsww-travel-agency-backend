from inspect import isclass
from typing import Any

from factory import Factory, faker
from src.example.infrastructure.storage.documents import Example


def is_factory(obj: Any) -> bool:
    return isclass(obj) and issubclass(obj, Factory) and not obj._meta.abstract


class ExampleFactory(Factory):
    class Meta:
        model = Example

    uniq_id = faker.Faker("uuid4")
    title = faker.Faker("sentence")
    author = faker.Faker("last_name")
