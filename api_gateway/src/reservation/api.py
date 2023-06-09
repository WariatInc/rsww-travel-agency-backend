from http import HTTPStatus
from uuid import UUID

import requests
from flask import Config, make_response
from requests.exceptions import ConnectionError
from webargs.flaskparser import use_kwargs

from src.api import Resource
from src.api.blueprint import Blueprint
from src.api.error import custom_error
from src.auth.login import auth_required, current_user
from src.consts import ReservationApiEndpoints
from src.domain.factories import actor_dto_factory
from src.reservation.domain.exceptions import TripOfferServiceUnavailable
from src.reservation.domain.ports import (
    IEnrichReservationsWithOffersDataCommand,
    IGetUsersPreferencesQuery,
)
from src.reservation.error import ERROR
from src.reservation.schema import (
    ReservationEventDashboardGetSchema,
    ReservationPostSchema,
)


class ReservationsResource(Resource):
    def __init__(
        self,
        config: Config,
        enrich_reservations_with_offers_data_command: IEnrichReservationsWithOffersDataCommand,
    ) -> None:
        self.reservation_service_root_url = config.get(
            "RESERVATION_SERVICE_ROOT_URL"
        )
        self.enrich_reservations_with_offers_data_command = (
            enrich_reservations_with_offers_data_command
        )

    @auth_required
    @use_kwargs(ReservationPostSchema)
    def post(self, offer_id: UUID, **kwargs):
        actor = actor_dto_factory(current_user)
        try:
            response = requests.post(
                url=f"{self.reservation_service_root_url}"
                f"{ReservationApiEndpoints.create_reservation}",
                json=dict(
                    user_gid=str(actor.gid),
                    offer_id=str(offer_id),
                    **kwargs,
                ),
            )
        except ConnectionError:
            return custom_error(
                ERROR.reservation_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)

    @auth_required
    def get(self):
        actor = actor_dto_factory(current_user)
        try:
            response = requests.get(
                url=f"{self.reservation_service_root_url}"
                f"{ReservationApiEndpoints.get_reservations.format(user_gid=actor.gid)}"
            )
        except ConnectionError:
            return custom_error(
                ERROR.reservation_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        try:
            enriched_reservations = (
                self.enrich_reservations_with_offers_data_command(
                    reservations=response.json()["reservations"]
                )
            )
        except TripOfferServiceUnavailable:
            return custom_error(
                ERROR.trip_offer_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )
        return make_response(enriched_reservations, response.status_code)


class ReservationCancelResource(Resource):
    def __init__(self, config: Config) -> None:
        self.reservation_service_root_url = config.get(
            "RESERVATION_SERVICE_ROOT_URL"
        )

    @auth_required
    def post(self, reservation_id: UUID):
        actor = actor_dto_factory(current_user)
        try:
            response = requests.post(
                url=f"{self.reservation_service_root_url}"
                f"{ReservationApiEndpoints.cancel_reservation.format(reservation_id=str(reservation_id))}",
                json=dict(user_gid=str(actor.gid)),
            )
        except ConnectionError:
            return custom_error(
                ERROR.reservation_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class ReservationResource(Resource):
    def __init__(self, config: Config) -> None:
        self.reservation_service_root_url = config.get(
            "RESERVATION_SERVICE_ROOT_URL"
        )

    @auth_required
    def get(self, reservation_id: UUID):
        actor = actor_dto_factory(current_user)
        try:
            response = requests.get(
                url=f"{self.reservation_service_root_url}"
                f"{ReservationApiEndpoints.get_reservation.format(reservation_id=reservation_id, user_gid=actor.gid)}",
            )
        except ConnectionError:
            return custom_error(
                ERROR.reservation_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)

    @auth_required
    def delete(self, reservation_id: UUID):
        actor = actor_dto_factory(current_user)
        try:
            response = requests.delete(
                url=f"{self.reservation_service_root_url}"
                f"{ReservationApiEndpoints.delete_reservation.format(reservation_id=reservation_id, user_gid=actor.gid)}",
            )
        except ConnectionError:
            return custom_error(
                ERROR.reservation_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(response.json(), response.status_code)


class ReservationEventDashboardResource(Resource):
    def __init__(self, config: Config) -> None:
        self.reservation_service_root_url = config.get(
            "RESERVATION_SERVICE_ROOT_URL"
        )

    @auth_required
    @use_kwargs(ReservationEventDashboardGetSchema, location="query")
    def get(self, **kwargs):
        try:
            response = requests.get(
                url=f"{self.reservation_service_root_url}"
                f"{ReservationApiEndpoints.get_reservation_events_dashboard}",
                params=kwargs,
            )
        except ConnectionError:
            return custom_error(
                ERROR.reservation_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )
        return make_response(response.json(), response.status_code)


class UserPreferencesResource(Resource):
    def __init__(
        self,
        config: Config,
        get_users_preferences_query: IGetUsersPreferencesQuery,
    ) -> None:
        self.reservation_service_root_url = config.get(
            "RESERVATION_SERVICE_ROOT_URL"
        )
        self.get_users_preferences_query = get_users_preferences_query

    def get(self):
        try:
            response = requests.get(
                url=f"{self.reservation_service_root_url}"
                f"{ReservationApiEndpoints.get_reserved_offers_ids}",
            )
        except ConnectionError:
            return custom_error(
                ERROR.reservation_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        try:
            preferences = self.get_users_preferences_query.get(
                response.json()["offers_ids"]
            )
        except TripOfferServiceUnavailable:
            return custom_error(
                ERROR.trip_offer_service_unavailable,
                HTTPStatus.SERVICE_UNAVAILABLE,
            )

        return make_response(
            preferences,
            response.status_code,
        )


class Api(Blueprint):
    name = "reservations"
    import_name = __name__

    resources = [
        (ReservationsResource, "/"),
        (ReservationCancelResource, "/cancel/<uuid:reservation_id>"),
        (ReservationResource, "/<uuid:reservation_id>"),
        (ReservationEventDashboardResource, "/events"),
        (UserPreferencesResource, "/preferences"),
    ]
