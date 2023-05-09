import sqlalchemy as sqla
from src.consts import PaymentItem, PaymentState
from src.extensions import db


class Payment(db.BaseModel):
    __tablename__ = "payment"
    __table_args__ = (sqla.PrimaryKeyConstraint("id", name="payment_pkey"),)

    id = db.Column(db.UUID())
    item_id = db.Column(db.UUID(), nullable=False)
    item = db.Column(db.Enum(PaymentItem), nullable=False)
    state = db.Column(db.Enum(PaymentState), nullable=False)
