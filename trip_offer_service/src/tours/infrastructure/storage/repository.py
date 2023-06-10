from uuid import UUID

from pymongo.collection import Collection

from src.consts import Collections
from src.infrastructure.storage import MongoClient
from src.tours.domain.ports import ITourRepository


class TourRepository(ITourRepository):
    def __init__(self, client: MongoClient) -> None:
        self.db = client.get_db()
        self.collection: Collection = self.db[Collections.tour]

    def upsert_tour(self, tour_id: UUID, **upsert_kwargs) -> None:
        self.collection.update_one(
            {"id": str(tour_id)},
            {
                "$set": upsert_kwargs,
                "$setOnInsert": {"tour_id": str(tour_id)},
            },
            upsert=True,
        )
