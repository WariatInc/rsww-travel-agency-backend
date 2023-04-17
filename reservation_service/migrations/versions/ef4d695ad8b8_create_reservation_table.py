"""Create reservation table

Revision ID: ef4d695ad8b8
Revises: 6e80b58d4007
Create Date: 2023-04-16 21:55:21.344035

"""
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from alembic import op

# revision identifiers, used by Alembic.
revision = "ef4d695ad8b8"
down_revision = "6e80b58d4007"
branch_labels = None
depends_on = None


reservation_state = psql.ENUM(
    "pending",
    "rejected",
    "accepted",
    "cancelled",
    name="reservation_state",
    create_type=True,
)


def upgrade():
    op.create_table(
        "reservation",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("offer_id", sa.UUID(), nullable=False),
        sa.Column("state", reservation_state, nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("_created", sa.DateTime(), nullable=True),
        sa.Column("_updated", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name="reservation_user_fkey",
            onupdate="NO ACTION",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="reservation_pkey"),
    )
    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.create_index(
            "ix_reservation_user_id_fkey", ["user_id"], unique=False
        )

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.create_unique_constraint("user_gid_unique", ["gid"])


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_constraint("user_gid_unique", type_="unique")

    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.drop_index("ix_reservation_user_id_fkey")

    op.drop_table("reservation")
