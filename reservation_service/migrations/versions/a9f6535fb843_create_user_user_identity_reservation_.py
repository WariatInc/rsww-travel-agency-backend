"""Create user user_identity reservation tables

Revision ID: a9f6535fb843
Revises: 
Create Date: 2023-04-18 19:26:31.143431

"""
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from alembic import op

# revision identifiers, used by Alembic.
revision = "a9f6535fb843"
down_revision = None
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
        "user_identity",
        sa.Column("gid", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("_created", sa.DateTime(), nullable=True),
        sa.Column("_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("gid", name="user_identity_pkey"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("gid", sa.UUID(), nullable=False),
        sa.Column("_created", sa.DateTime(), nullable=True),
        sa.Column("_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
        sa.UniqueConstraint("gid", name="user_gid_unique"),
    )
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
            ["users.id"],
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


def downgrade():
    with op.batch_alter_table("reservation", schema=None) as batch_op:
        batch_op.drop_index("ix_reservation_user_id_fkey")

    op.drop_table("reservation")
    op.drop_table("users")
    op.drop_table("user_identity")
