import marshmallow as ma

from src.offer.infrastructure.queries.search import SearchOptions
from src.offer.infrastructure.storage.offer import Offer, SimpleOffer


class SearchOptionsSchema(ma.Schema):
    page = ma.fields.Int()
    operator = ma.fields.Str()
    country = ma.fields.Str()
    city = ma.fields.Str()
    date_start = ma.fields.Date()
    date_end = ma.fields.Date()
    transport = ma.fields.Str()
    adults = ma.fields.Int()
    kids = ma.fields.Int()
    room = ma.fields.Str()
    available = ma.fields.Bool()

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
    city = ma.fields.Str()
    transport = ma.fields.Str()
    number_of_adults = ma.fields.Int()
    number_of_kids = ma.fields.Int()
    room_type = ma.fields.Str()
    is_available = ma.fields.Bool()

    @ma.post_load
    def create_offer(self, data, **_):
        return Offer(**data)


class SimpleOfferSchema(ma.Schema):
    offer_id = ma.fields.UUID()
    tour_id = ma.fields.UUID()
    operator = ma.fields.Str()
    country = ma.fields.Str()
    city = ma.fields.Str()
    thumbnail_url = ma.fields.Str()
    arrival_date = ma.fields.Raw()
    departure_date = ma.fields.Raw()
    is_available = ma.fields.Bool()

    @ma.post_load
    def create_offer(self, data, **_):
        return SimpleOffer(**data)
