from uuid import UUID

from src.offers.domain.dtos import OfferEnrichmentDataDto
from src.offers.domain.ports import IGetOfferEnrichmentDataQuery, IOffersView


class GetOfferEnrichmentDataQuery(IGetOfferEnrichmentDataQuery):
    def __init__(self, offers_view: IOffersView) -> None:
        self._offers_view = offers_view

    def get(
        self, offers_ids: list[UUID]
    ) -> dict[UUID, OfferEnrichmentDataDto]:
        offers = self._offers_view.get_offer_views_by_offer_ids(
            [str(offer_id) for offer_id in offers_ids]
        )
        return {
            offer.offer_id: OfferEnrichmentDataDto(
                hotel=offer.hotel,
                city=offer.city,
                arrival_date=offer.arrival_date,
                departure_date=offer.departure_date,
                thumbnail_url=offer.thumbnail_url,
                country=offer.country,
                room_type=offer.room_type,
            )
            for offer in offers
        }
