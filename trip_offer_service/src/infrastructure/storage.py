from typing import TYPE_CHECKING

from flask import Config
from pymongo import MongoClient as _MongoClient

if TYPE_CHECKING:
    from pymongo.database import Database


class MongoClient:
    def __init__(self, config: Config) -> None:
        db_name = config["MONGO_DB_NAME"]

        self.client = _MongoClient(
            config["MONGO_URI"],
            uuidRepresentation="standard"
        )
        self.db = getattr(self.client, db_name)

    def get_db(self) -> "Database":
        return self.db


class MongoReadOnlyClient:
    def __init__(self, config: Config) -> None:
        db_name = config["MONGO_DB_NAME"]

        print(config["MONGO_READONLY_URI"])
        self.client = _MongoClient(
            config["MONGO_READONLY_URI"],
            uuidRepresentation="standard"
        )
        self.db = getattr(self.client, db_name)

    def get_db(self) -> "Database":
        return self.db
