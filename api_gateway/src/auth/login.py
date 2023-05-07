from functools import wraps
from http import HTTPStatus
from typing import Callable

from flask import g, request
from werkzeug.local import LocalProxy

from src.api.error import custom_error
from src.auth.error import ERROR
from src.extensions import db
from src.user.infrastructure.storage.models import User

current_user = LocalProxy(lambda: _get_current_user())


def _get_current_user():
    return g.current_user


def _get_auth_info() -> bool:
    if auth_email := request.headers.get("Authorization"):
        g.auth_email = auth_email
        return True
    return False


def auth_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not _get_auth_info():
            return custom_error(ERROR.unauthorized, HTTPStatus.UNAUTHORIZED)

        if not (
            user := db.session.query(User)
            .filter(User.email == g.auth_email)
            .one_or_none()
        ):
            return custom_error(
                ERROR.user_wrong_credentials, HTTPStatus.UNAUTHORIZED
            )

        g.current_user = user
        return func(*args, **kwargs)

    return wrapper
