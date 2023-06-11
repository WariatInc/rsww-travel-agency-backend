import marshmallow as ma

from src.api.schema import non_nullable, possibly_undefined_non_nullable


class UpdateUserSessionPostSchema(ma.Schema):
    webapp_page = ma.fields.String(**non_nullable)
    session_id = ma.fields.UUID(**possibly_undefined_non_nullable)


class UserSessionOnGivenPageGetSchema(ma.Schema):
    webapp_page = ma.fields.String(**non_nullable)


class UserSessionsOnGivenPageSchema(ma.Schema):
    user_sessions_count = ma.fields.Integer(**non_nullable)


class UserSessionRevokeDeleteSchema(ma.Schema):
    session_id = ma.fields.UUID(**non_nullable)
