from functools import wraps
from http import HTTPStatus
from typing import Callable

from flask import Response, make_response
from marshmallow import Schema, missing

non_nullable = dict(required=True, allow_none=False)
explicitly_nullable = dict(required=True, allow_none=True)
implicitly_nullable = dict(
    required=False, allow_none=True, load_default=None, dump_default=None
)
possibly_undefined_nullable = dict(
    required=False, allow_none=True, load_default=missing, dump_default=missing
)
possibly_undefined_non_nullable = dict(
    required=False,
    allow_none=False,
    load_default=missing,
    dump_default=missing,
)


def use_schema(schema: type[Schema], code: HTTPStatus) -> Callable:
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs) -> Callable:
            data = f(*args, **kwargs)
            return make_response(schema().dumps(data), code)

        return wrapper

    return decorator


class EmptySchema(Schema):
    pass
