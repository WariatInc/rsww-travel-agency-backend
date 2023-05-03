from typing import Optional
from uuid import UUID

import marshmallow as ma

from src.consts import Collections
from src.infrastructure.storage import MongoReadOnlyClient
from src.offer.domain.ports import IGetOfferQuery
from src.offer.infrastructure.storage.offer import Offer
from src.offer.schema import OfferSchema


class GetOfferQuery(IGetOfferQuery):
    def __init__(self, client: MongoReadOnlyClient) -> None:
        self.collection_name = Collections.offer_view
        self.client = client

    def get_offer(self, offer_id: UUID) -> Optional[Offer]:
        result = self.client.get_db()[self.collection_name].find_one(
            {"offer_id": str(offer_id)}
        )

        return (
            OfferSchema().load(result, unknown=ma.EXCLUDE) if result else None
        )
