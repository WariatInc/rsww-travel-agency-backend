from uuid import uuid4

from src.extensions import db


class UserIdentity(db.BaseModel):
    __tablename__ = "user_identity"

    __table_args__ = (
        db.PrimaryKeyConstraint("gid", name="user_identity_pkey"),
    )

    gid = db.Column(db.UUID(), default=uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)


class User(db.BaseModel):
    __tablename__ = "users"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="user_pkey"),
        db.UniqueConstraint("gid", name="user_gid_unique"),
    )

    id = db.Column(db.UUID(), nullable=False, default=uuid4)
    gid = db.Column(db.UUID(), nullable=False)
    reservations = db.relationship("Reservation", back_populates="user")
