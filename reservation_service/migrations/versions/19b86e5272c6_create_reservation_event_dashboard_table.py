"""Create reservation_event_dashboard table

Revision ID: 19b86e5272c6
Revises: 3f5056ec1109
Create Date: 2023-06-02 18:47:32.616794

"""
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from alembic import op

# revision identifiers, used by Alembic.
revision = "19b86e5272c6"
down_revision = "3f5056ec1109"
branch_labels = None
depends_on = None


reservation_state = psql.ENUM(
    "pending",
    "rejected",
    "accepted",
    "cancelled",
    name="reservation_state",
    create_type=False,
)


def upgrade():
    op.create_table(
        "reservation_event_dashboard",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("reservation_id", sa.UUID(), nullable=False),
        sa.Column("offer_id", sa.UUID(), nullable=False),
        sa.Column("state", reservation_state, nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="reservation_event_dashboard_pkey"),
    )


def downgrade():
    op.drop_table("reservation_event_dashboard")
