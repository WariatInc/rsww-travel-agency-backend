"""Create tour and offer tables

Revision ID: 274a3fc473e4
Revises:
Create Date: 2023-04-20 21:11:23.501948

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql as psql

# revision identifiers, used by Alembic.
revision = "274a3fc473e4"
down_revision = None
branch_labels = None
depends_on = None

room_type_enum = psql.ENUM(
    "standard",
    "family",
    "apartment",
    "studio",
    name="room_type_enum",
    create_type=True,
)

transport_type_enum = psql.ENUM(
    "self", "plane", "bus", name="transport_type_enum", create_type=True
)


def upgrade() -> None:
    op.create_table(
        "tour",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("operator", sa.String(), nullable=False),
        sa.Column("hotel", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("thumbnail_url", sa.String(), nullable=False),
        sa.Column("score", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="tour_pkey"),
    )
    op.create_table(
        "offer",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("arrival_date", sa.Date(), nullable=False),
        sa.Column("departure_date", sa.Date(), nullable=False),
        sa.Column("departure_city", sa.String(), nullable=True),
        sa.Column("transport", transport_type_enum, nullable=False),
        sa.Column("number_of_adults", sa.SmallInteger(), nullable=False),
        sa.Column("number_of_kids", sa.SmallInteger(), nullable=False),
        sa.Column("room_type", room_type_enum, nullable=False),
        sa.Column("available", sa.Boolean(), nullable=False),
        sa.Column("tour_id", sa.UUID(), nullable=False),
        sa.CheckConstraint("number_of_adults >= 0", name="valid_adults"),
        sa.CheckConstraint("number_of_kids >= 0", name="valid_kids"),
        sa.ForeignKeyConstraint(
            ["tour_id"],
            ["tour.id"],
            name="offer_tour_fkey",
            onupdate="NO ACTION",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="offer_pkey"),
    )
    op.create_index(
        "ix_offer_tour_id_fkey", "offer", ["tour_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_offer_tour_id_fkey", table_name="offer")
    op.drop_table("offer")
    op.drop_table("tour")
