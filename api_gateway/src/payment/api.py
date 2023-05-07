from http import HTTPStatus
from uuid import UUID

import requests
from flask import Config, make_response
from requests.exceptions import ConnectionError
from webargs.flaskparser import use_kwargs

from src.api import Resource
from src.api.blueprint import Blueprint
from src.api.error import custom_error
from src.auth.login import auth_required
from src.consts import PaymentApiEndpoints
from src.payment.error import ERROR
from src.payment.schema import ProcessPaymentSchema


class PaymentReservationResource(Resource):
    def __init__(self, config: Config) -> None:
        self.payment_service_root_url = config.get("PAYMENT_SERVICE_ROOT_URL")

    @auth_required
    @use_kwargs(ProcessPaymentSchema, location="json")
    def post(self, item_id: UUID):
        try:
            response = requests.post(
                url=f"{self.payment_service_root_url}"
                f"{PaymentApiEndpoints.process_reservation_payment}",
                json=dict(item_id=str(item_id)),
            )
        except ConnectionError:
            return custom_error(
                ERROR.payment_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class Api(Blueprint):
    name = "payment"
    import_name = __name__

    resources = [(PaymentReservationResource, "/reservation")]
