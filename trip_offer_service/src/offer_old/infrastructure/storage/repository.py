from uuid import UUID

from pymongo.collection import Collection

from src.consts import Collections
from src.infrastructure.storage import MongoClient
from src.offer_old.domain.ports import IOfferRepository
from src.offer_old.infrastructure.storage.documents import Offer


class OfferRepository(IOfferRepository):
    def __init__(self, client: MongoClient) -> None:
        self.db = client.get_db()
        self.collection: Collection[Offer] = self.db[Collections.offer_view]

    def upsert_offer(self, offer_id: UUID, **upsert_kwargs) -> None:
        self.collection.update_one(
            {"offer_id": str(offer_id)},
            {
                "$set": upsert_kwargs,
                "$setOnInsert": {"offer_id": str(offer_id)},
            },
            upsert=True,
        )
