from typing import Optional

from flask import Flask
from flask_injector import FlaskInjector, FlaskModule
from injector import Injector, inject

from src.config import Config, DefaultConfig
from src.di_container.modules import all_modules
from src.utils import import_from

__all__ = ["create_app"]


def create_app(
    app_name: Optional[str] = None, config: Optional[Config] = None
) -> Flask:
    """Create Flask app"""

    if not app_name:
        app_name = DefaultConfig.PROJECT

    app = Flask(
        app_name,
        instance_relative_config=True,
        static_url_path="/admin/custom/static",
        static_folder="static",
    )

    configure_app(app, config)
    configure_injector(app)
    configure_blueprints(app)
    configure_extensions(app)

    return app


def configure_app(app: Flask, config: Optional[Config]) -> None:
    app.config.from_object(DefaultConfig)

    if config:
        app.config.from_object(config)


def configure_extensions(app: Flask) -> None:
    FlaskInjector(app, injector=app.injector)


def configure_injector(app: Flask) -> Injector:
    app.injector = Injector(auto_bind=False, modules=all_modules)
    app.injector.binder.install(FlaskModule(app=app))
    return app.injector


def configure_blueprints(app: Flask) -> None:
    for module in app.config.get("BLUEPRINTS"):
        blueprint = import_from(module, "Api")
        inject(blueprint.__init__)
        instance = app.injector.create_object(blueprint)
        instance.register()
