import os


class Config:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class DefaultConfig(Config):
    ENVIRONMENT = "dev"
    PROJECT = "trip_offer_service"
    TESTING = False

    MONGO_DB_NAME = os.environ.get("MONGO_DB")
    MONGO_URI = "mongodb://{user}:{password}@{host}:{port}/{db_name}".format(
        user=os.environ.get("MONGO_USER"),
        password=os.environ.get("MONGO_PASSWORD"),
        host=os.environ.get("MONGO_HOST"),
        port=os.environ.get("MONGO_PORT"),
        db_name=MONGO_DB_NAME,
    )
    MONGO_READONLY_URI = (
        "mongodb://{user}_readonly:{password}@{host}:{port}/{db_name}".format(
            user=os.environ.get("MONGO_USER"),
            password=os.environ.get("MONGO_PASSWORD"),
            host=os.environ.get("MONGO_HOST"),
            port=os.environ.get("MONGO_PORT"),
            db_name=MONGO_DB_NAME,
        )
    )

    MONGO_VIEW_COLLECTION_NAME = "offer_view"

    BLUEPRINTS = ["src.offer.api"]

    RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
    RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT")
    RABBITMQ_USER = os.environ.get("RABBITMQ_USER")
    RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD")


class ProductionConfig(DefaultConfig):
    ENVIRONMENT = "prod"
    CONSUMERS = ["src.offer.infrastructure.message_broker.consumer"]


class TestConfig(DefaultConfig):
    ENVIRONMENT = "test"
    TESTING = True

    MONGO_DB_NAME = "trip_offer_test_mongo"
    MONGO_URI = "mongodb://trip_offer_test:trip_offer_test@mongo_db:27017/trip_offer_test_mongo"
