from uuid import uuid4

from src.consts import ReservationState
from src.extensions import db


class Reservation(db.BaseModel):
    __tablename__ = "reservation"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="reservation_pkey"),
        db.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="reservation_user_fkey",
            ondelete="CASCADE",
            onupdate="NO ACTION",
        ),
        db.Index("ix_reservation_user_id_fkey", "user_id"),
    )

    id = db.Column(db.UUID(), nullable=False, default=uuid4)
    offer_id = db.Column(db.UUID(), nullable=False)
    state = db.Column(
        db.Enum(ReservationState, name="reservation_state"),
        nullable=False,
        default=ReservationState.pending,
    )

    user_id = db.Column(db.UUID(), nullable=False)
    user = db.relationship("User", back_populates="reservations")

    rejection_reason = db.Column(db.String(), nullable=True)
