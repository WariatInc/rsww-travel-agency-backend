import marshmallow as ma

from src.api.schema import non_nullable


class ProcessPaymentSchema(ma.Schema):
    item_id = ma.fields.UUID(**non_nullable)
