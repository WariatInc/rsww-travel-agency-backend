from http import HTTPStatus
from typing import Union
from uuid import UUID

from flask import Response
from webargs.flaskparser import use_kwargs

from src.api.blueprint import Blueprint, Resource
from src.api.error import custom_error
from src.api.schema import use_schema
from src.auth.login import auth_required
from src.reservation.domain.exceptions import (
    ActorIsNotReservationOwner,
    ReservationAlreadyCancelled,
    ReservationExistInPendingOrAcceptedStateException,
    ReservationNotFound,
)
from src.reservation.domain.ports import (
    ICancelReservationCommand,
    ICreateReservationCommand,
    IGetUserReservationsQuery,
)
from src.reservation.error import ERROR
from src.reservation.schema import ReservationListSchema, ReservationPostSchema


class ReservationsResource(Resource):
    def __init__(
        self,
        create_reservation_command: ICreateReservationCommand,
        get_user_reservations_query: IGetUserReservationsQuery,
    ) -> None:
        self.create_reservation_command = create_reservation_command
        self.get_user_reservations_query = get_user_reservations_query

    @auth_required
    @use_kwargs(ReservationPostSchema, location="json")
    def post(self, offer_id: UUID) -> Union[Response, tuple[dict, int]]:
        try:
            self.create_reservation_command(offer_id)
        except ReservationExistInPendingOrAcceptedStateException:
            return custom_error(
                ERROR.reservation_exist_in_pending_or_accepted_state_error.value,
                HTTPStatus.BAD_REQUEST,
            )

        return {}, HTTPStatus.CREATED

    @auth_required
    @use_schema(ReservationListSchema, HTTPStatus.OK)
    def get(self):
        return {"reservations": self.get_user_reservations_query.get()}


class ReservationCancelResource(Resource):
    def __init__(
        self, cancel_reservation_command: ICancelReservationCommand
    ) -> None:
        self.cancel_reservation_command = cancel_reservation_command

    @auth_required
    def post(self, reservation_id: UUID) -> Union[Response, tuple[dict, int]]:
        try:
            self.cancel_reservation_command(reservation_id)
        except ReservationAlreadyCancelled:
            return custom_error(
                ERROR.reservation_already_cancelled_error,
                HTTPStatus.BAD_REQUEST,
            )
        except ReservationNotFound:
            return custom_error(
                ERROR.reservation_not_found_error, HTTPStatus.BAD_REQUEST
            )
        except ActorIsNotReservationOwner:
            return custom_error(
                ERROR.actor_is_not_reservation_owner_error,
                HTTPStatus.BAD_REQUEST,
            )

        return {}, HTTPStatus.OK


class Api(Blueprint):
    name = "reservations"
    import_name = __name__

    resources = [
        (ReservationsResource, "/"),
        (ReservationCancelResource, "/<uuid:reservation_id>/cancel"),
    ]
