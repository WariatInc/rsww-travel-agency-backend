import marshmallow as ma

from src.api.schema import non_nullable


class UpdateUserSessionPostSchema(ma.Schema):
    webapp_page = ma.fields.String(**non_nullable)


class UserSessionOnGivenPageGetSchema(ma.Schema):
    webapp_page = ma.fields.String(**non_nullable)


class UserSessionsOnGivenPageSchema(ma.Schema):
    user_sessions_count = ma.fields.Integer(**non_nullable)
