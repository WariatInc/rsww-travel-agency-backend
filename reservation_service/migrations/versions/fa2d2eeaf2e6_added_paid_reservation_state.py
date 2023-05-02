"""Added paid reservation state

Revision ID: fa2d2eeaf2e6
Revises: a9f6535fb843
Create Date: 2023-05-02 12:37:46.448553

"""
from src.utils import alter_enum

# revision identifiers, used by Alembic.
revision = "fa2d2eeaf2e6"
down_revision = "a9f6535fb843"
branch_labels = None
depends_on = None


old_reservation_state = ["pending", "rejected", "accepted", "cancelled"]

new_reservation_state = [
    "pending",
    "rejected",
    "accepted",
    "cancelled",
    "paid",
]


def upgrade():
    alter_enum(
        table="reservation",
        column_name="state",
        enum_name="reservation_state",
        old_options=old_reservation_state,
        new_options=new_reservation_state,
    )


def downgrade():
    alter_enum(
        table="reservation",
        column_name="status",
        enum_name="reservation_state",
        old_options=new_reservation_state,
        new_options=old_reservation_state,
    )
