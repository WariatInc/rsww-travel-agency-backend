import marshmallow as ma

from src.tour.domain.dtos import TourDto
from src.consts import TransportType


class TourSchema(ma.Schema):
    id = ma.fields.UUID()
    city = ma.fields.Str()
    country = ma.fields.Str()
    hotel = ma.fields.Str()
    description = ma.fields.Str()
    thumbnail_url = ma.fields.Str()
    arrival_date = ma.fields.Raw()
    departure_date = ma.fields.Raw()
    departure_city = ma.fields.String(allow_none=True)
    transport = ma.fields.Enum(TransportType)

    @ma.post_load
    def create_tour(self, data, **_):
        return TourDto(**data)
