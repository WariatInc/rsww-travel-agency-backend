from typing import Iterable

from flask import Flask
from injector import inject

from src.api import Resource
from src.utils import has_constructor_defined


class Blueprint:
    BLUEPRINT_URL_PREFIX = "/api/{endpoint}"

    def __init__(self, app: Flask) -> None:
        self._app = app

    @property
    def name(self) -> str:
        return getattr(self, "name")

    @property
    def import_name(self) -> str:
        return getattr(self, "import_name")

    @property
    def resources(self) -> Iterable[tuple[Resource, str]]:
        return getattr(self, "resources", [])

    def _add_api_resource(self, resource: Resource, url: str) -> None:
        endpoint = f"{self.name}{url}"
        self._app.add_url_rule(
            self.BLUEPRINT_URL_PREFIX.format(endpoint=endpoint),
            view_func=resource.as_view(
                self.name.capitalize() + resource.__name__
            ),
        )

    def register(self) -> None:
        for resource, url in self.resources:
            self._add_api_resource(resource, url)

            if has_constructor_defined(resource):
                inject(resource.__init__)
                self._app.injector.create_object(resource)
