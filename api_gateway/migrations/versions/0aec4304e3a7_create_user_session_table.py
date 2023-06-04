"""Create user session table

Revision ID: 0aec4304e3a7
Revises: ee499acd875b
Create Date: 2023-06-03 20:11:41.568297

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0aec4304e3a7"
down_revision = "ee499acd875b"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_session",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("ip_address", sa.String(), nullable=False),
        sa.Column("webapp_page", sa.String(), nullable=True),
        sa.Column("expires_in", sa.Integer(), nullable=False),
        sa.Column("refreshed_at", sa.DateTime(), nullable=False),
        sa.Column("_created", sa.DateTime(), nullable=True),
        sa.Column("_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="user_session_pkey"),
    )


def downgrade():
    op.drop_table("user_session")
