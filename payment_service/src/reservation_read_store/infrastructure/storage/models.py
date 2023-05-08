import sqlalchemy as sqla

from src.consts import ReservationState
from src.extensions import db


class ReservationReadStore(db.BaseModel):
    __tablename__ = "reservation_read_store"
    __table_args__ = (
        sqla.PrimaryKeyConstraint(
            "reservation_id", name="reservation_read_store_pkey"
        ),
    )

    reservation_id = db.Column(db.UUID())
    state = db.Column(db.Enum(ReservationState), nullable=False)
    price = db.Column(db.Float(), nullable=True)
