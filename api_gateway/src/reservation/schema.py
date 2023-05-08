import marshmallow as ma

from src.api.schema import non_nullable


class ReservationPostSchema(ma.Schema):
    offer_id = ma.fields.UUID(**non_nullable)
