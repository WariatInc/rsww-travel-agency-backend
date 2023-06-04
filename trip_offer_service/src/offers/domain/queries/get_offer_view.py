from typing import Any
from uuid import UUID

from src.offers.domain.ports import IOffersView, IQueryOffer
from src.offer.domain.dtos import OfferViewDto


class InspectOfferQuery(IQueryOffer):
    def __init__(self, view: IOffersView) -> None:
        self.view = view

    def __call__(self, offer_id: UUID) -> OfferViewDto:
        return self.view.inspect(offer_id)
