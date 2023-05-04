import marshmallow as ma

from src.api.schema import non_nullable
from src.consts import ReservationState


class ReservationPostSchema(ma.Schema):
    offer_id = ma.fields.UUID(**non_nullable)


class ReservationSchema(ma.Schema):
    id = ma.fields.UUID(**non_nullable)
    offer_id = ma.fields.UUID(**non_nullable)
    user_id = ma.fields.UUID(**non_nullable)
    state = ma.fields.Enum(ReservationState, **non_nullable)


class ReservationListSchema(ma.Schema):
    reservations = ma.fields.Nested(
        ReservationSchema, many=True, **non_nullable
    )


class CreatedReservationSchema(ma.Schema):
    reservation_id = ma.fields.UUID()
