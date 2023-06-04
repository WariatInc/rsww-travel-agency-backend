import marshmallow as ma

from src.api.schema import non_nullable, possibly_undefined_non_nullable


class ReservationPostSchema(ma.Schema):
    offer_id = ma.fields.UUID(**non_nullable)
    kids_up_to_3 = ma.fields.Integer(
        **possibly_undefined_non_nullable, validate=lambda x: x >= 0
    )
    kids_up_to_10 = ma.fields.Integer(
        **possibly_undefined_non_nullable, validate=lambda x: x >= 0
    )


class ReservationEventDashboardGetSchema(ma.Schema):
    page = ma.fields.Integer(
        validate=lambda x: x > 0, **possibly_undefined_non_nullable
    )
    query = ma.fields.Integer(
        validate=lambda x: x > 0, **possibly_undefined_non_nullable
    )
