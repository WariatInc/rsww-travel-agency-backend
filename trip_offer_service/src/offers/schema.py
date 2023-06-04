import marshmallow as ma

from src.api.schema import possibly_undefined_non_nullable
from src.consts import RoomType
from src.offers.domain.dtos import SearchOptions


class SearchOptionsSchema(ma.Schema):
    page = ma.fields.Integer(
        validate=lambda x: x >= 1, **possibly_undefined_non_nullable
    )
    tour_id = ma.fields.UUID(required=True)
    room_type = ma.fields.Enum(RoomType, **possibly_undefined_non_nullable)
    adults = ma.fields.Integer(
        validate=lambda x: x >= 0, **possibly_undefined_non_nullable
    )
    kids = ma.fields.Integer(
        validate=lambda x: x >= 0, **possibly_undefined_non_nullable
    )
    all_inclusive = ma.fields.Bool(**possibly_undefined_non_nullable)
    breakfast = ma.fields.Bool(**possibly_undefined_non_nullable)

    @ma.post_load
    def create_search_options(self, data, **_):
        return SearchOptions(**data)
