from http import HTTPStatus
from uuid import UUID

from src.api import Resource
from src.api.blueprint import Blueprint
from src.api.error import custom_error
from src.api.schema import use_schema
from src.payment.domain.exceptions import (
    ItemAlreadyPaid,
    ItemCannotBePaid,
    ItemNotFound,
    ItemPaymentInProgress,
)
from src.payment.domain.ports import IProcessReservationPaymentCommand
from src.payment.error import ERROR
from src.payment.schema import (
    ProcessReservationPaymentPostSchema,
    ProcessReservationPaymentSchema,
)
from webargs.flaskparser import use_kwargs


class ProcessReservationPaymentResource(Resource):
    def __init__(
        self,
        process_reservation_payment_command: IProcessReservationPaymentCommand,
    ):
        self._process_reservation_payment_command = (
            process_reservation_payment_command
        )

    @use_schema(ProcessReservationPaymentSchema, HTTPStatus.OK)
    @use_kwargs(ProcessReservationPaymentPostSchema, location="json")
    def post(self, item_id: UUID):
        try:
            result = self._process_reservation_payment_command(item_id)
        except ItemAlreadyPaid:
            return custom_error(
                ERROR.item_already_paid, HTTPStatus.BAD_REQUEST
            )
        except ItemCannotBePaid:
            return custom_error(
                ERROR.item_cannot_be_paid, HTTPStatus.BAD_REQUEST
            )
        except ItemNotFound:
            return custom_error(ERROR.item_not_found, HTTPStatus.NOT_FOUND)
        except ItemPaymentInProgress:
            return custom_error(
                ERROR.item_payment_in_progress, HTTPStatus.BAD_REQUEST
            )

        return {"result": result}


class Api(Blueprint):
    name = "payment"
    import_name = __name__

    resources = [(ProcessReservationPaymentResource, "/reservation")]
