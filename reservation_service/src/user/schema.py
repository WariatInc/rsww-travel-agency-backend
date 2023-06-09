import marshmallow as ma

from src.api.schema import non_nullable


class UserSchema(ma.Schema):
    id = ma.fields.UUID(**non_nullable)
    gid = ma.fields.UUID(**non_nullable)
