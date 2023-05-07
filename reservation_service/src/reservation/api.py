from http import HTTPStatus
from uuid import UUID

from webargs.flaskparser import use_kwargs

from src.api.blueprint import Blueprint, Resource
from src.api.error import custom_error
from src.api.schema import EmptySchema, use_schema
from src.reservation.domain.exceptions import (
    ReservationAlreadyCancelled,
    ReservationCannotBeDeleted,
    ReservationExistInPendingAcceptedOrPaidStateException,
    ReservationIsPaid,
    ReservationNotFound,
    UserIsNotReservationOwner,
)
from src.reservation.domain.ports import (
    ICancelReservationCommand,
    ICreateReservationCommand,
    IDeleteRejectedReservationCommand,
    IGetReservationQuery,
    IGetUserReservationsQuery,
)
from src.reservation.error import ERROR
from src.reservation.schema import (
    CreatedReservationSchema,
    ReservationCancelPostSchema,
    ReservationDeleteSchema,
    ReservationGetSchema,
    ReservationListSchema,
    ReservationPostSchema,
    ReservationSchema,
    ReservationsGetSchema,
)
from src.user.domain.exceptions import UserNotFoundException


class ReservationsResource(Resource):
    def __init__(
        self,
        create_reservation_command: ICreateReservationCommand,
        get_user_reservations_query: IGetUserReservationsQuery,
    ) -> None:
        self.create_reservation_command = create_reservation_command
        self.get_user_reservations_query = get_user_reservations_query

    @use_schema(CreatedReservationSchema, HTTPStatus.OK)
    @use_kwargs(ReservationPostSchema, location="json")
    def post(self, user_gid: UUID, offer_id: UUID):
        try:
            reservation = self.create_reservation_command(user_gid, offer_id)
        except ReservationExistInPendingAcceptedOrPaidStateException:
            return custom_error(
                ERROR.reservation_exist_in_pending_accepted_or_paid_state_error,
                HTTPStatus.BAD_REQUEST,
            )
        except UserNotFoundException:
            return custom_error(
                ERROR.user_not_found_error, HTTPStatus.NOT_FOUND
            )

        return {"reservation_id": reservation.id}

    @use_schema(ReservationListSchema, HTTPStatus.OK)
    @use_kwargs(ReservationsGetSchema, location="query")
    def get(self, user_gid: UUID):
        return {"reservations": self.get_user_reservations_query.get(user_gid)}


class ReservationCancelResource(Resource):
    def __init__(
        self, cancel_reservation_command: ICancelReservationCommand
    ) -> None:
        self.cancel_reservation_command = cancel_reservation_command

    @use_schema(EmptySchema, HTTPStatus.OK)
    @use_kwargs(ReservationCancelPostSchema, location="json")
    def post(self, user_gid: UUID, reservation_id: UUID):
        try:
            self.cancel_reservation_command(user_gid, reservation_id)
        except ReservationAlreadyCancelled:
            return custom_error(
                ERROR.reservation_already_cancelled_error,
                HTTPStatus.BAD_REQUEST,
            )
        except ReservationNotFound:
            return custom_error(
                ERROR.reservation_not_found_error, HTTPStatus.NOT_FOUND
            )
        except UserIsNotReservationOwner:
            return custom_error(
                ERROR.user_is_not_reservation_owner_error,
                HTTPStatus.FORBIDDEN,
            )
        except ReservationIsPaid:
            return custom_error(
                ERROR.reservation_is_paid_cannot_be_cancelled,
                HTTPStatus.BAD_REQUEST,
            )
        except UserNotFoundException:
            return custom_error(
                ERROR.user_not_found_error, HTTPStatus.NOT_FOUND
            )

        return {}


class ReservationResource(Resource):
    def __init__(
        self,
        delete_rejected_reservation_command: IDeleteRejectedReservationCommand,
        get_reservation_query: IGetReservationQuery,
    ) -> None:
        self.delete_rejected_reservation_command = (
            delete_rejected_reservation_command
        )
        self.get_reservation_query = get_reservation_query

    @use_kwargs(ReservationGetSchema, location="query")
    @use_schema(ReservationSchema, HTTPStatus.OK)
    def get(self, user_gid: UUID, reservation_id: UUID):
        try:
            reservation = self.get_reservation_query.get(
                user_gid, reservation_id
            )
        except UserNotFoundException:
            return custom_error(
                ERROR.user_not_found_error, HTTPStatus.NOT_FOUND
            )
        except ReservationNotFound:
            return custom_error(
                ERROR.reservation_not_found_error, HTTPStatus.NOT_FOUND
            )

        return reservation

    @use_schema(EmptySchema, HTTPStatus.OK)
    @use_kwargs(ReservationDeleteSchema, location="query")
    def delete(self, user_gid: UUID, reservation_id: UUID):
        try:
            self.delete_rejected_reservation_command(user_gid, reservation_id)
        except ReservationNotFound:
            return custom_error(
                ERROR.reservation_not_found_error, HTTPStatus.NOT_FOUND
            )
        except ReservationCannotBeDeleted:
            return custom_error(
                ERROR.reservation_cannot_be_deleted, HTTPStatus.BAD_REQUEST
            )
        except UserIsNotReservationOwner:
            return custom_error(
                ERROR.user_is_not_reservation_owner_error,
                HTTPStatus.FORBIDDEN,
            )
        except UserNotFoundException:
            return custom_error(
                ERROR.user_not_found_error, HTTPStatus.NOT_FOUND
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
