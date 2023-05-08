import json
from http import HTTPStatus
from typing import Optional

from flask import Response, make_response
from werkzeug.utils import Headers


def custom_error(
    msg: str,
    code=HTTPStatus.INTERNAL_SERVER_ERROR,
    headers: Optional[Headers] = None,
    **kwargs,
) -> Response:
    data = dict(message=msg)
    data.update(kwargs)
    response = make_response(
        json.dumps(data), code, {"Content-Type": "application/json"}
    )
    if headers:
        response.headers.extend(headers)

    return response


def validation_error(errors: dict[str, list[str]]) -> Response:
    return make_response(
        json.dumps(dict(messages=errors)),
        HTTPStatus.UNPROCESSABLE_ENTITY,
        {"Content-Type": "application/json"},
    )
