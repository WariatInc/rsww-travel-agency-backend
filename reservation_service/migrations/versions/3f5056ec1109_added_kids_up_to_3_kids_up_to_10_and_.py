"""Added kids_up_to_3 kids_up_to_10 and price columns to reservation

Revision ID: 3f5056ec1109
Revises: 049918e6915f
Create Date: 2023-05-08 21:46:59.389066

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3f5056ec1109"
down_revision = "049918e6915f"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("kids_up_to_3", sa.Integer(), nullable=False)
        )
        batch_op.add_column(
            sa.Column("kids_up_to_10", sa.Integer(), nullable=False)
        )
        batch_op.add_column(sa.Column("price", sa.Float(), nullable=False))


def downgrade():
    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.drop_column("price")
        batch_op.drop_column("kids_up_to_10")
        batch_op.drop_column("kids_up_to_3")
