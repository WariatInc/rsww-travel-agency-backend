from http import HTTPStatus
from uuid import UUID

from webargs.flaskparser import use_kwargs

from src.api.blueprint import Blueprint, Resource
from src.api.error import custom_error
from src.api.schema import EmptySchema, use_schema
from src.auth.login import auth_required
from src.reservation.domain.exceptions import (
    ActorIsNotReservationOwner,
    ReservationAlreadyCancelled,
    ReservationCannotBeDeleted,
    ReservationExistInPendingAcceptedOrPaidStateException,
    ReservationIsPaid,
    ReservationNotFound,
)
from src.reservation.domain.ports import (
    ICancelReservationCommand,
    ICreateReservationCommand,
    IDeleteRejectedReservationCommand,
    IGetUserReservationsQuery,
)
from src.reservation.error import ERROR
from src.reservation.schema import (
    CreatedReservationSchema,
    ReservationListSchema,
    ReservationPostSchema,
)


class ReservationsResource(Resource):
    def __init__(
        self,
        create_reservation_command: ICreateReservationCommand,
        get_user_reservations_query: IGetUserReservationsQuery,
    ) -> None:
        self.create_reservation_command = create_reservation_command
        self.get_user_reservations_query = get_user_reservations_query

    @auth_required
    @use_schema(CreatedReservationSchema, HTTPStatus.OK)
    @use_kwargs(ReservationPostSchema, location="json")
    def post(self, offer_id: UUID):
        try:
            reservation = self.create_reservation_command(offer_id)
        except ReservationExistInPendingAcceptedOrPaidStateException:
            return custom_error(
                ERROR.reservation_exist_in_pending_accepted_or_paid_state_error.value,
                HTTPStatus.BAD_REQUEST,
            )

        return {"reservation_id": reservation.id}

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
    @use_schema(EmptySchema, HTTPStatus.OK)
    def post(self, reservation_id: UUID):
        try:
            self.cancel_reservation_command(reservation_id)
        except ReservationAlreadyCancelled:
            return custom_error(
                ERROR.reservation_already_cancelled_error,
                HTTPStatus.BAD_REQUEST,
            )
        except ReservationNotFound:
            return custom_error(
                ERROR.reservation_not_found_error, HTTPStatus.NOT_FOUND
            )
        except ActorIsNotReservationOwner:
            return custom_error(
                ERROR.actor_is_not_reservation_owner_error,
                HTTPStatus.FORBIDDEN,
            )
        except ReservationIsPaid:
            return custom_error(
                ERROR.reservation_is_paid_cannot_be_cancelled,
                HTTPStatus.BAD_REQUEST,
            )

        return {}


class ReservationResource(Resource):
    def __init__(
        self,
        delete_rejected_reservation_command: IDeleteRejectedReservationCommand,
    ) -> None:
        self.delete_rejected_reservation_command = (
            delete_rejected_reservation_command
        )

    @auth_required
    @use_schema(EmptySchema, HTTPStatus.OK)
    def delete(self, reservation_id: UUID):
        try:
            self.delete_rejected_reservation_command(reservation_id)
        except ReservationNotFound:
            return custom_error(
                ERROR.reservation_not_found_error, HTTPStatus.NOT_FOUND
            )
        except ReservationCannotBeDeleted:
            return custom_error(
                ERROR.reservation_cannot_be_deleted, HTTPStatus.BAD_REQUEST
            )
        except ActorIsNotReservationOwner:
            return custom_error(
                ERROR.actor_is_not_reservation_owner_error,
                HTTPStatus.FORBIDDEN,
            )

        return {}


class Api(Blueprint):
    name = "reservations"
    import_name = __name__

    resources = [
        (ReservationsResource, "/"),
        (ReservationResource, "/<uuid:reservation_id>"),
        (ReservationCancelResource, "/cancel/<uuid:reservation_id>"),
    ]
