"""alter reservation.price column to nullable

Revision ID: 9a4cb019db46
Revises: 19b86e5272c6
Create Date: 2023-06-02 21:25:35.441421

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9a4cb019db46"
down_revision = "19b86e5272c6"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.alter_column(
            "price",
            existing_type=sa.DOUBLE_PRECISION(precision=53),
            nullable=True,
        )


def downgrade():
    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.alter_column(
            "price",
            existing_type=sa.DOUBLE_PRECISION(precision=53),
            nullable=False,
        )
