"""Create reservation_read_store table

Revision ID: 39d3a5821d2e
Revises:
Create Date: 2023-05-01 21:33:33.980072

"""
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from alembic import op

# revision identifiers, used by Alembic.
revision = "39d3a5821d2e"
down_revision = None
branch_labels = None
depends_on = None


reservation_state_enum = psql.ENUM(
    "accepted",
    "rejected",
    "pending",
    "cancelled",
    "paid",
    name="reservation_state_enum",
    create_type=True,
)


def upgrade():
    op.create_table(
        "reservation_read_store",
        sa.Column("reservation_id", sa.UUID(), nullable=False),
        sa.Column("state", reservation_state_enum, nullable=False),
        sa.Column("_created", sa.DateTime(), nullable=True),
        sa.Column("_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint(
            "reservation_id", name="reservation_read_store_pkey"
        ),
    )


def downgrade():
    op.drop_table("reservation_read_store")
