from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.offer.domain.factories import offer_dto_factory
from src.offer.domain.ports import IOfferRepository
from src.offer.infrastructure.storage.models import Offer

if TYPE_CHECKING:
    from src.offer.domain.dtos import OfferDto


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

    def check_if_offer_can_be_reserved(self, offer_id: UUID) -> bool:
        return self._session.query(
            self._session.query(Offer)
            .filter(Offer.id == offer_id, Offer.available)
            .exist()
        ).scalar()
