from http import HTTPStatus
from threading import Thread
from typing import Optional

from flask import Flask, Response
from flask_injector import FlaskInjector, FlaskModule
from injector import Injector, inject

from src.api.error import validation_error
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
    configure_handlers(app)

    if app.config.get("ENVIRONMENT") == "prod":
        configure_consumers(app)

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


def configure_consumers(app: Flask) -> None:
    for module in app.config.get("CONSUMERS"):
        consume_func = import_from(module, "consume")
        consumer = Thread(target=consume_func, args=(app.config,), daemon=True)
        consumer.start()


def configure_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
    def handle_unprocessable_entity(err: Exception) -> Response:
        exc = getattr(err, "exc")
        messages = getattr(exc, "messages", None)
        return validation_error(messages)
