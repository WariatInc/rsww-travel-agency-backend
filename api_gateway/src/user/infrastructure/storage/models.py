from uuid import uuid4

from src.extensions import db


class User(db.BaseModel):
    __tablename__ = "users"

    __table_args__ = (db.PrimaryKeyConstraint("gid", name="user_pkey"),)

    gid = db.Column(db.UUID(), default=uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
