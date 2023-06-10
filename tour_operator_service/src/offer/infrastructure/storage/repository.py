from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID

import sqlalchemy as sqla
from sqlalchemy.orm import Session

from src.offer.domain.factories import offer_dto_factory, tour_dto_factory
from src.offer.domain.ports import IOfferRepository, ITourRepository
from src.offer.infrastructure.storage.models import Offer, Tour

if TYPE_CHECKING:
    from src.offer.domain.dtos import OfferDto, TourDto


class OfferRepository(IOfferRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def update_offer(
        self, offer_id: UUID, update_dict: dict[str, Any]
    ) -> None:
        self._session.query(Offer).filter(Offer.id == offer_id).update(
            update_dict
        )

    def get_offer(self, offer_id: UUID) -> Optional["OfferDto"]:
        if (
            offer := self._session.query(Offer)
            .filter(Offer.id == offer_id)
            .one_or_none()
        ):
            return offer_dto_factory(offer)

    def get_random_offer(self) -> "OfferDto":
        offer = (
            self._session.query(Offer)
            .filter(Offer.available)
            .order_by(sqla.func.random())
            .first()
        )
        return offer_dto_factory(offer)

    def get_offers_by_tour_id(self, tour_id: UUID) -> list["OfferDto"]:
        return [
            offer_dto_factory(offer)
            for offer in self._session.query(Offer)
            .filter(Offer.tour_id == tour_id, Offer.available)
            .all()
        ]

    def check_if_offer_can_be_reserved(self, offer_id: UUID) -> bool:
        return self._session.query(
            self._session.query(Offer)
            .filter(Offer.id == offer_id, Offer.available)
            .exists()
        ).scalar()


class TourRepository(ITourRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def update_tour(self, tour_id: UUID, update_dict: dict[str, Any]) -> None:
        self._session.query(Tour).filter(Tour.id == tour_id).update(
            update_dict
        )

    def get_random_tour(self) -> "TourDto":
        tour = self._session.query(Tour).order_by(sqla.func.random()).first()
        return tour_dto_factory(tour)

    def get_tour(self, tour_id: UUID) -> Optional["TourDto"]:
        if (
            tour := self._session.query(Tour)
            .filter(Tour.id == tour_id)
            .one_or_none()
        ):
            return tour_dto_factory(tour)
