"""add cancel_reason column to reservation table

Revision ID: f02dea045b85
Revises: 9a4cb019db46
Create Date: 2023-06-10 18:34:01.182199

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql as psql

# revision identifiers, used by Alembic.
revision = "f02dea045b85"
down_revision = "9a4cb019db46"
branch_labels = None
depends_on = None


cancel_reason_enum = psql.ENUM(
    "payment_timeout",
    "cancelled_by_user",
    name="cancel_reason_enum",
    create_type=True,
)


def upgrade():
    cancel_reason_enum.create(op.get_bind())
    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("cancel_reason", cancel_reason_enum, nullable=True)
        )


def downgrade():
    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.drop_column("cancel_reason")
