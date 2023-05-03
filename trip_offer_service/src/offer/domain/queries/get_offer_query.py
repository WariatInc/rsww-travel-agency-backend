from uuid import UUID
from typing import Optional

import marshmallow as ma

from src.infrastructure.storage import MongoReadOnlyClient
from src.offer.domain.ports import IGetOfferQuery
from src.offer.infrastructure.storage.offer import Offer
from src.consts import Collections
from src.offer.schema import OfferSchema


class GetOfferQuery(IGetOfferQuery):
    def __init__(self, client: MongoReadOnlyClient) -> None:
        self.collection_name = Collections.offer_view
        self.client = client

    def get_offer(self, offer_id: UUID) -> Optional[Offer]:
        schema = OfferSchema()
        result = self.client.get_db()[self.collection_name].find_one(
            {"offer_id": str(offer_id)}
        )
        return result if result is None else schema.load(result, unknown=ma.EXCLUDE)
