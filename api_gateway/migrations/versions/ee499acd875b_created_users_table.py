"""Created users table

Revision ID: ee499acd875b
Revises:
Create Date: 2023-05-06 18:45:00.664625

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ee499acd875b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("gid", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("_created", sa.DateTime(), nullable=True),
        sa.Column("_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("gid", name="user_pkey"),
    )


def downgrade():
    op.drop_table("users")
