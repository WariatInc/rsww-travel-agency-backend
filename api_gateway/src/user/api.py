from http import HTTPStatus
from typing import Optional
from uuid import UUID

from flask import Response, make_response, request
from webargs.flaskparser import use_kwargs

from src.api import Resource
from src.api.blueprint import Blueprint
from src.user.domain.ports import (
    IGetUserOnGivenPageCountQuery,
    IRevokeUserSessionCommand,
    IUpdateUserSessionCommand,
)
from src.user.schema import (
    UpdateUserSessionPostSchema,
    UserSessionOnGivenPageGetSchema,
    UserSessionRevokeDeleteSchema,
    UserSessionsOnGivenPageSchema,
)


class UserSessionResource(Resource):
    def __init__(
        self,
        update_user_session_command: IUpdateUserSessionCommand,
        revoke_user_session_command: IRevokeUserSessionCommand,
    ) -> None:
        self._update_user_session_command = update_user_session_command
        self._revoke_user_session_command = revoke_user_session_command

    @use_kwargs(UpdateUserSessionPostSchema, location="json")
    def post(
        self, webapp_page: str, session_id: Optional[UUID] = None
    ) -> Response:
        ip_address = request.environ.get(
            "HTTP_X_FORWARDED_FOR", request.remote_addr
        )
        session_id = self._update_user_session_command(
            ip_address=ip_address,
            webapp_page=webapp_page,
            session_id=session_id,
        )
        return make_response({"session_id": session_id}, HTTPStatus.OK)

    @use_kwargs(UserSessionRevokeDeleteSchema, location="json")
    def delete(self, session_id: UUID) -> Response:
        self._revoke_user_session_command(session_id)
        return make_response({}, HTTPStatus.OK)


class UserSessionOnGivenPageResource(Resource):
    def __init__(
        self, get_user_on_given_page_count_query: IGetUserOnGivenPageCountQuery
    ) -> None:
        self._get_user_on_given_page_count_query = (
            get_user_on_given_page_count_query
        )

    @use_kwargs(UserSessionOnGivenPageGetSchema, location="query")
    def get(self, webapp_page: str) -> Response:
        user_sessions_count = self._get_user_on_given_page_count_query.get(
            webapp_page
        )
        return make_response(
            UserSessionsOnGivenPageSchema().dumps(
                {"user_sessions_count": user_sessions_count}
            ),
            HTTPStatus.OK,
        )


class Api(Blueprint):
    name = "users"
    import_name = __name__

    resources = [
        (UserSessionResource, "/sessions"),
        (UserSessionOnGivenPageResource, "/sessions/page"),
    ]
