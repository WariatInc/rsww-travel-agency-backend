import marshmallow as ma

from src.api.schema import possibly_undefined_non_nullable
from src.consts import RoomType, TransportType
from src.offer_old.domain.dtos import OfferDto, SearchOptions, SimpleOfferDto


class SearchOptionsSchema(ma.Schema):
    page = ma.fields.Integer(
        validate=lambda x: x >= 1, **possibly_undefined_non_nullable
    )
    operator = ma.fields.Str(**possibly_undefined_non_nullable)
    country = ma.fields.Str(**possibly_undefined_non_nullable)
    city = ma.fields.Str(**possibly_undefined_non_nullable)
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

    @ma.post_load
    def create_search_options(self, data, **_):
        return SearchOptions(**data)


class OfferSchema(ma.Schema):
    offer_id = ma.fields.UUID()
    tour_id = ma.fields.UUID()
    operator = ma.fields.Str()
    country = ma.fields.Str()
    city = ma.fields.Str()
    description = ma.fields.Str()
    thumbnail_url = ma.fields.Str()
    arrival_date = ma.fields.Raw()
    departure_date = ma.fields.Raw()
    departure_city = ma.fields.String(allow_none=True)
    transport = ma.fields.Enum(TransportType)
    number_of_adults = ma.fields.Integer()
    number_of_kids = ma.fields.Integer()
    room_type = ma.fields.Enum(RoomType)
    is_available = ma.fields.Bool()

    @ma.post_load
    def create_offer(self, data, **_):
        return OfferDto(**data)


class SimpleOfferSchema(ma.Schema):
    offer_id = ma.fields.UUID()
    tour_id = ma.fields.UUID()
    operator = ma.fields.String()
    country = ma.fields.String()
    city = ma.fields.String()
    thumbnail_url = ma.fields.Str()
    arrival_date = ma.fields.Raw()
    departure_date = ma.fields.Raw()
    departure_city = ma.fields.String(allow_none=True)
    transport = ma.fields.Enum(TransportType)
    number_of_adults = ma.fields.Integer()
    number_of_kids = ma.fields.Integer()
    room_type = ma.fields.Enum(RoomType)
    is_available = ma.fields.Bool()
    price = ma.fields.Float(allow_none=True, default=None)

    @ma.post_load
    def create_offer(self, data, **_):
        return SimpleOfferDto(**data)


class OfferPriceSchema(ma.Schema):
    price = ma.fields.Float()


class OfferPriceGetSchema(ma.Schema):
    kids_up_to_3 = ma.fields.Integer(
        **possibly_undefined_non_nullable, validate=lambda x: x >= 0
    )
    kids_up_to_10 = ma.fields.Integer(
        **possibly_undefined_non_nullable, validate=lambda x: x >= 0
    )
