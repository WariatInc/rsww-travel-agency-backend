import marshmallow as ma

from src.offer.domain.dtos import OfferDto, OfferViewDto
from src.consts import RoomType, TransportType


class OfferSchema(ma.Schema):
    id = ma.fields.UUID()
    tour_id = ma.fields.UUID()
    number_of_adults = ma.fields.Int()
    number_of_kids = ma.fields.Int()
    room_type = ma.fields.Enum(RoomType)
    all_inclusive = ma.fields.Bool()
    breakfast = ma.fields.Bool()
    is_available = ma.fields.Bool()

    @ma.post_load
    def create_tour(self, data, **_):
        return OfferDto(**data)


class OfferViewSchema(ma.Schema):
    offer_id = ma.fields.UUID()
    tour_id = ma.fields.UUID()
    number_of_adults = ma.fields.Int()
    number_of_kids = ma.fields.Int()
    room_type = ma.fields.Enum(RoomType)
    all_inclusive = ma.fields.Bool()
    breakfast = ma.fields.Bool()
    is_available = ma.fields.Bool()
    country = ma.fields.Str()
    operator = ma.fields.Str()
    city = ma.fields.Str()
    hotel = ma.fields.Str()
    description = ma.fields.Str()
    thumbnail_url = ma.fields.Str()
    arrival_date = ma.fields.Raw()
    departure_date = ma.fields.Raw()
    departure_city = ma.fields.String(allow_none=True)
    transport = ma.fields.Enum(TransportType)

    @ma.post_load
    def create_offer_view(self, data, **_):
        return OfferViewDto(**data)
