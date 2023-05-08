"""Added rejection reason column

Revision ID: 049918e6915f
Revises: fa2d2eeaf2e6
Create Date: 2023-05-05 16:33:51.208328

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "049918e6915f"
down_revision = "fa2d2eeaf2e6"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("rejection_reason", sa.String(), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.drop_column("rejection_reason")
