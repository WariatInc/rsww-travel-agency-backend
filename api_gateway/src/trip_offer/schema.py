import marshmallow as ma
from src.api.schema import possibly_undefined_non_nullable
from src.consts import RoomType, TransportType


class SearchOfferSchema(ma.Schema):
    page = ma.fields.Integer(
        validate=lambda x: x >= 1, **possibly_undefined_non_nullable
    )
    operator = ma.fields.String(**possibly_undefined_non_nullable)
    country = ma.fields.String(**possibly_undefined_non_nullable)
    city = ma.fields.String(**possibly_undefined_non_nullable)
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
    room = ma.fields.Enum(RoomType, **possibly_undefined_non_nullable)


class OfferPriceGetSchema(ma.Schema):
    kids_up_to_3 = ma.fields.Integer(
        **possibly_undefined_non_nullable, validate=lambda x: x >= 0
    )
    kids_up_to_10 = ma.fields.Integer(
        **possibly_undefined_non_nullable, validate=lambda x: x >= 0
    )
