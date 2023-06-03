from uuid import uuid4

import sqlalchemy as sqla
import sqlalchemy.orm as orm

from src.consts import RoomType, Transport
from src.extensions import Base


class Tour(Base):
    __tablename__ = "tour"
    __table_args__ = (sqla.PrimaryKeyConstraint("id", name="tour_pkey"),)

    id = orm.mapped_column(sqla.UUID(), default=uuid4)
    operator = orm.mapped_column(sqla.String(), nullable=False)
    hotel = orm.mapped_column(sqla.String(), nullable=False)
    country = orm.mapped_column(sqla.String(), nullable=False)
    departure_city = orm.mapped_column(sqla.String(), nullable=False)
    description = orm.mapped_column(sqla.Text())
    thumbnail_url = orm.mapped_column(sqla.String(), nullable=False)
    arrival_date = orm.mapped_column(sqla.DateTime(), nullable=False)
    departure_date = orm.mapped_column(sqla.DateTime(), nullable=False)
    transport = orm.mapped_column(
        sqla.Enum(Transport, name="transport_type_enum"), nullable=False
    )
    average_night_cost = orm.mapped_column(sqla.Float(), nullable=False)
    average_flight_cost = orm.mapped_column(sqla.Float(), nullable=False)
    offers = orm.relationship("Offer", back_populates="tour")


class Offer(Base):
    __tablename__ = "offer"
    __table_args__ = (
        sqla.PrimaryKeyConstraint("id", name="offer_pkey"),
        sqla.ForeignKeyConstraint(
            ["tour_id"],
            ["tour.id"],
            name="offer_tour_fkey",
            ondelete="CASCADE",
            onupdate="NO ACTION",
        ),
        sqla.Index("ix_offer_tour_id_fkey", "tour_id"),
        sqla.CheckConstraint("number_of_adults >= 0", name="valid_adults"),
        sqla.CheckConstraint("number_of_kids >= 0", name="valid_kids"),
    )

    id = orm.mapped_column(sqla.UUID(), default=uuid4)
    number_of_adults = orm.mapped_column(sqla.SmallInteger(), nullable=False)
    number_of_kids = orm.mapped_column(sqla.SmallInteger(), nullable=False)
    room_type = orm.mapped_column(
        sqla.Enum(RoomType, name="room_type_enum"), nullable=False
    )
    all_inclusive = orm.mapped_column(
        sqla.Boolean(), nullable=False, default=False
    )
    breakfast = orm.mapped_column(
        sqla.Boolean(), nullable=False, default=False
    )
    available = orm.mapped_column(sqla.Boolean(), nullable=False)

    tour_id = orm.mapped_column(sqla.UUID(), nullable=False)
    tour = orm.relationship("Tour", back_populates="offers")
