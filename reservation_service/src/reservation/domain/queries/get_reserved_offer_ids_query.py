from uuid import UUID

from src.reservation.domain.ports import (
    IGetReservedOffersQuery,
    IReservedOffersView,
)


class GetReservedOffersQuery(IGetReservedOffersQuery):
    def __init__(self, reserved_offers_view: IReservedOffersView) -> None:
        self._reserved_offers_view = reserved_offers_view

    def get(self) -> list[UUID]:
        return [
            reservation.offer_id
            for reservation in self._reserved_offers_view.get_reserved_offers()
        ]
