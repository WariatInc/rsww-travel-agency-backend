import marshmallow as ma

from src.offer.domain.dtos import OfferDto
from src.consts import RoomType


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
