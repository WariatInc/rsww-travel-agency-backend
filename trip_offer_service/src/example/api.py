from http import HTTPStatus
from uuid import UUID

from flask import jsonify
from webargs.flaskparser import use_kwargs

from src.api import Resource
from src.api.blueprint import Blueprint
from src.example.domain.ports import (
    IGetExamplesListQuery,
    IUpsertExampleCommand,
)
from src.example.schema import ExampleUpsertSchema


class ExampleResource(Resource):
    def __init__(self, upsert_example_command: IUpsertExampleCommand) -> None:
        self.upsert_example_command = upsert_example_command

    @use_kwargs(ExampleUpsertSchema, location="json")
    def post(self, uniq_id: UUID, **kwargs):
        self.upsert_example_command(uniq_id=uniq_id, **kwargs)
        return jsonify({}), HTTPStatus.CREATED


class ExamplesResource(Resource):
    def __init__(self, get_example_list_query: IGetExamplesListQuery) -> None:
        self.get_example_list_query = get_example_list_query

    def get(self):
        return jsonify(self.get_example_list_query()), HTTPStatus.OK


class Api(Blueprint):
    name = "examples"
    import_name = __name__

    resources = [
        (ExampleResource, "/example/<uuid:uniq_id>"),
        (ExamplesResource, "/"),
    ]
