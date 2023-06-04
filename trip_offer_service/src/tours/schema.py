import marshmallow as ma

from src.api.schema import possibly_undefined_non_nullable
from src.consts import TransportType
from src.tours.domain.dtos import SearchOptions


class SearchOptionsSchema(ma.Schema):
    page = ma.fields.Integer(
        validate=lambda x: x >= 1, **possibly_undefined_non_nullable
    )
    country = ma.fields.Str(**possibly_undefined_non_nullable)
    operator = ma.fields.Str(**possibly_undefined_non_nullable)
    date_start = ma.fields.Date(**possibly_undefined_non_nullable)
    date_end = ma.fields.Date(**possibly_undefined_non_nullable)
    transport = ma.fields.Enum(
        TransportType, **possibly_undefined_non_nullable
    )
    adults = ma.fields.Integer(
        validate=lambda x: x >= 0, **possibly_undefined_non_nullable
    )
    kids = ma.fields.Integer(
        validate=lambda x: x >= 0, **possibly_undefined_non_nullable
    )
    departure_city = ma.fields.Str(**possibly_undefined_non_nullable)

    @ma.post_load
    def create_search_options(self, data, **_):
        return SearchOptions(**data)