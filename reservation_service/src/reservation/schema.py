import marshmallow as ma

from src.api.schema import (
    explicitly_nullable,
    non_nullable,
    possibly_undefined_non_nullable,
)
from src.consts import CancelReason, ReservationState
from src.user.schema import UserSchema


class ReservationPostSchema(ma.Schema):
    offer_id = ma.fields.UUID(**non_nullable)
    user_gid = ma.fields.UUID(**non_nullable)
    kids_up_to_3 = ma.fields.Integer(
        **possibly_undefined_non_nullable, validate=lambda x: x >= 0
    )
    kids_up_to_10 = ma.fields.Integer(
        **possibly_undefined_non_nullable, validate=lambda x: x >= 0
    )


class ReservationSchema(ma.Schema):
    id = ma.fields.UUID(**non_nullable)
    offer_id = ma.fields.UUID(**non_nullable)
    user = ma.fields.Nested(UserSchema, **non_nullable)
    state = ma.fields.Enum(ReservationState, **non_nullable)
    rejection_reason = ma.fields.String(**explicitly_nullable)
    cancel_reason = ma.fields.Enum(CancelReason, **explicitly_nullable)
    price = ma.fields.Float(**non_nullable)


class ReservationDetailsSchema(ma.Schema):
    id = ma.fields.UUID(**non_nullable)
    offer_id = ma.fields.UUID(**non_nullable)
    user = ma.fields.Nested(UserSchema, **non_nullable)
    state = ma.fields.Enum(ReservationState, **non_nullable)
    rejection_reason = ma.fields.String(**explicitly_nullable)
    cancel_reason = ma.fields.Enum(CancelReason, **explicitly_nullable)
    kids_up_to_3 = ma.fields.Integer(**non_nullable)
    kids_up_to_10 = ma.fields.Integer(**non_nullable)
    price = ma.fields.Float(**non_nullable)


class ReservationGetSchema(ma.Schema):
    user_gid = ma.fields.UUID(**non_nullable)


class ReservationListSchema(ma.Schema):
    reservations = ma.fields.Nested(
        ReservationSchema, many=True, **non_nullable
    )


class CreatedReservationSchema(ma.Schema):
    reservation_id = ma.fields.UUID()


class ReservationsGetSchema(ma.Schema):
    user_gid = ma.fields.UUID(**non_nullable)


class ReservationCancelPostSchema(ma.Schema):
    user_gid = ma.fields.UUID(**non_nullable)


class ReservationDeleteSchema(ma.Schema):
    user_gid = ma.fields.UUID(**non_nullable)


class ReservationEventDashboardGetSchema(ma.Schema):
    page = ma.fields.Integer(
        validate=lambda x: x > 0, **possibly_undefined_non_nullable
    )
    size = ma.fields.Integer(
        validate=lambda x: x > 0, **possibly_undefined_non_nullable
    )


class ReservationEventDashboardSchema(ma.Schema):
    id = ma.fields.UUID(**non_nullable)
    reservation_id = ma.fields.UUID(**non_nullable)
    offer_id = ma.fields.UUID(**non_nullable)
    state = ma.fields.Enum(ReservationState, **non_nullable)
    timestamp = ma.fields.DateTime(**non_nullable)


class ReservationEventDashboardListSchema(ma.Schema):
    reservation_events = ma.fields.Nested(
        ReservationEventDashboardSchema, many=True, **non_nullable
    )
    total_pages = ma.fields.Integer(**non_nullable)
