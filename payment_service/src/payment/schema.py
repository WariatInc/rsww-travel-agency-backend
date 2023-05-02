import marshmallow as ma

from src.api.schema import non_nullable
from src.consts import PaymentState


class ProcessReservationPaymentPostSchema(ma.Schema):
    item_id = ma.fields.UUID(**non_nullable)


class ProcessReservationPaymentSchema(ma.Schema):
    result = ma.fields.Enum(PaymentState, **non_nullable)
