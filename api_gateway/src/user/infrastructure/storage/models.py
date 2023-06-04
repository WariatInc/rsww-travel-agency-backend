from datetime import datetime, timedelta
from uuid import uuid4

import sqlalchemy as sqla
from sqlalchemy.ext.hybrid import hybrid_property

from src.consts import USER_SESSION_EXPIRE_IN
from src.extensions import db
from src.utils import get_current_time


class User(db.BaseModel):
    __tablename__ = "users"

    __table_args__ = (db.PrimaryKeyConstraint("gid", name="user_pkey"),)

    gid = db.Column(db.UUID(), default=uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)


class UserSession(db.BaseModel):
    __tablename__ = "user_session"
    __table_args__ = (db.PrimaryKeyConstraint("id", name="user_session_pkey"),)

    id = db.Column(db.UUID(), default=uuid4)
    ip_address = db.Column(db.String(), nullable=False)
    webapp_page = db.Column(db.String(), nullable=True)
    expires_in = db.Column(db.Integer(), nullable=False)
    refreshed_at = db.Column(
        db.DateTime(), nullable=False, default=get_current_time
    )
    user_logout = db.Column(db.Boolean(), nullable=False, default=False)

    @hybrid_property
    def revoked(self) -> bool:
        return any(
            [
                self.refreshed_at + timedelta(seconds=self.expires_in)
                < get_current_time(),
                self.user_logout,
            ]
        )

    @revoked.expression
    def revoked(self) -> sqla.sql.ColumnElement:
        return sqla.or_(
            self.refreshed_at
            + sqla.text(f"INTERVAL '{USER_SESSION_EXPIRE_IN} seconds'")
            + sqla.literal(datetime.min.time())
            < get_current_time(),
            self.user_logout,
        ).label("revoked")
