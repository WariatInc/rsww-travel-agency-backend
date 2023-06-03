from uuid import UUID

from src.offer.domain.ports import IGetOfferPriceQuery, IOfferPriceView


class GetOfferPriceQuery(IGetOfferPriceQuery):
    def __init__(self, offer_price_view: IOfferPriceView) -> None:
        self._offer_price_view = offer_price_view

    def get(
        self, offer_id: UUID, kids_up_to_3: int, kids_up_to_10: int
    ) -> float:
        return self._offer_price_view.get_offer_price(
            offer_id, kids_up_to_3, kids_up_to_10
        )
