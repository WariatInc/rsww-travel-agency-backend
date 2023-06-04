"""tour offer update

Revision ID: fdda3567f0c0
Revises: 274a3fc473e4
Create Date: 2023-05-18 18:38:32.951603

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql as psql

# revision identifiers, used by Alembic.
revision = "fdda3567f0c0"
down_revision = "274a3fc473e4"
branch_labels = None
depends_on = None


room_type_enum = psql.ENUM(
    "standard",
    "family",
    "apartment",
    "studio",
    name="room_type_enum",
    create_type=False,
)

transport_type_enum = psql.ENUM(
    "self", "plane", "bus", name="transport_type_enum", create_type=False
)


def upgrade() -> None:
    op.add_column(
        "offer", sa.Column("all_inclusive", sa.Boolean(), nullable=False)
    )
    op.add_column(
        "offer", sa.Column("breakfast", sa.Boolean(), nullable=False)
    )
    op.drop_column("offer", "departure_city")
    op.drop_column("offer", "transport")
    op.drop_column("offer", "departure_date")
    op.drop_column("offer", "arrival_date")
    op.drop_column("tour", "score")
    op.add_column(
        "tour", sa.Column("departure_city", sa.String(), nullable=False)
    )
    op.add_column(
        "tour", sa.Column("arrival_date", sa.DateTime(), nullable=False)
    )
    op.add_column(
        "tour", sa.Column("departure_date", sa.DateTime(), nullable=False)
    )
    op.add_column(
        "tour", sa.Column("transport", transport_type_enum, nullable=False)
    )
    op.add_column(
        "tour", sa.Column("average_night_cost", sa.Float(), nullable=False)
    )
    op.add_column(
        "tour", sa.Column("average_flight_cost", sa.Float(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("tour", "average_flight_cost")
    op.drop_column("tour", "average_night_cost")
    op.drop_column("tour", "transport")
    op.drop_column("tour", "departure_date")
    op.drop_column("tour", "arrival_date")
    op.drop_column("tour", "departure")
    op.add_column(
        "tour",
        sa.Column("score", sa.SmallInteger(), nullable=False, default=0),
    )
    op.add_column(
        "offer",
        sa.Column(
            "arrival_date", sa.DATE(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "offer",
        sa.Column(
            "departure_date", sa.DATE(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "offer",
        sa.Column(
            "transport",
            transport_type_enum,
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "offer",
        sa.Column(
            "departure_city", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    op.drop_column("offer", "breakfast")
    op.drop_column("offer", "all_inclusive")
