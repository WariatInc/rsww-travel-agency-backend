"""Added user_logout column to user session table

Revision ID: 3341d8e691e4
Revises: 0aec4304e3a7
Create Date: 2023-06-03 20:49:52.581004

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3341d8e691e4"
down_revision = "0aec4304e3a7"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user_session", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("user_logout", sa.Boolean(), nullable=False)
        )


def downgrade():
    with op.batch_alter_table("user_session", schema=None) as batch_op:
        batch_op.drop_column("user_logout")
