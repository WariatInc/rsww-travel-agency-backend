from datetime import datetime
from typing import Any

from pymongo.collection import Collection
from pymongo.database import Database

from src.example.domain.ports import IExampleRepository
from src.example.infrastructure.storage.documents import Example
from src.infrastructure.storage import MongoClient


class ExampleRepository(IExampleRepository):
    def __init__(self, mongo_client: MongoClient) -> None:
        self.db: Database = mongo_client.get_db()
        self.collection: Collection[Example] = self.db.example

    def upsert(self, data: dict[str, Any]) -> None:
        now = datetime.utcnow()
        to_upsert = dict(**data, _updated=now)

        self.collection.update_one(
            {"uniq_id": to_upsert["uniq_id"]},
            {"$set": to_upsert, "$setOnInsert": {"_created": now}},
            upsert=True,
        )
