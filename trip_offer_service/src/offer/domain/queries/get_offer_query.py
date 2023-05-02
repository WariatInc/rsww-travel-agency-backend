from uuid import UUID

from flask import Config

from src.infrastructure.storage import MongoReadOnlyClient
from src.offer.domain.ports import IGetOfferQuery
from src.offer.infrastructure.storage.offer import Offer


class GetOfferQuery(IGetOfferQuery):
    def __init__(self, config: Config, client: MongoReadOnlyClient) -> None:
        self.collection_name = config["MONGO_VIEW_COLLECTION_NAME"]
        self.client = client

    def get_offer(self, offer_id: UUID) -> Offer:
        result = self.client.get_db()[self.collection_name].find_one(
            {"offer_id": str(offer_id)}
        )

        assert result is not None
        return Offer.from_json(result)
