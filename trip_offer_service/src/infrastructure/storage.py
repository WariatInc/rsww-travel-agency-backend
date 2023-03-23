from typing import TYPE_CHECKING

from flask import Config
from pymongo import MongoClient as _MongoClient

if TYPE_CHECKING:
    from pymongo.database import Database


class MongoClient:
    def __init__(self, config: Config) -> None:
        self.client = _MongoClient(
            config["MONGO_URI"], uuidRepresentation="standard"
        )
        self.db_name = config["MONGO_DB_NAME"]

    def __call__(self) -> _MongoClient:
        return self.client

    def get_db(self) -> "Database":
        return getattr(self.client, self.db_name)


class MongoReadOnlyClient:
    def __init__(self, config: Config) -> None:
        self.client = _MongoClient(
            config["MONGO_READONLY_URI"], uuidRepresentation="standard"
        )
        self.db_name = config["MONGO_DB_NAME"]

    def __call__(self) -> _MongoClient:
        return self.client

    def get_db(self) -> "Database":
        return getattr(self.client, self.db_name)
