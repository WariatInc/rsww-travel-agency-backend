"""Added price column to payment

Revision ID: 6f82e8524155
Revises: 4fbabde2c019
Create Date: 2023-05-08 23:02:54.168408

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6f82e8524155"
down_revision = "4fbabde2c019"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table(
        "reservation_read_store", schema=None
    ) as batch_op:
        batch_op.add_column(sa.Column("price", sa.Float(), nullable=True))


def downgrade():
    with op.batch_alter_table(
        "reservation_read_store", schema=None
    ) as batch_op:
        batch_op.drop_column("price")
