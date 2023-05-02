"""Created payment table

Revision ID: 4fbabde2c019
Revises: 39d3a5821d2e
Create Date: 2023-05-01 23:46:02.432256

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql as psql

# revision identifiers, used by Alembic.
revision = "4fbabde2c019"
down_revision = "39d3a5821d2e"
branch_labels = None
depends_on = None


payment_item_enum = psql.ENUM(
    "reservation",
    name="payment_item_enum",
    create_type=True,
)

payment_state_enum = psql.ENUM(
    "finalized",
    "rejected",
    "pending",
    name="payment_state_enum",
    create_type=True,
)


def upgrade():
    op.create_table(
        "payment",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("item_id", sa.UUID(), nullable=False),
        sa.Column("item", payment_item_enum, nullable=False),
        sa.Column("state", payment_state_enum, nullable=False),
        sa.Column("_created", sa.DateTime(), nullable=True),
        sa.Column("_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="payment_pkey"),
    )


def downgrade():
    op.drop_table("payment")
