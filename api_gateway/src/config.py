import os


class Config:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class DefaultConfig(Config):
    ENVIRONMENT = "dev"
    PROJECT = "api_gateway"
    TESTING = False

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://{user}:{password}@{host}:{port}/{db}".format(
            user=os.environ.get("PG_USER"),
            password=os.environ.get("PG_PASSWORD"),
            host=os.environ.get("PG_HOST"),
            port=os.environ.get("PG_PORT"),
            db=os.environ.get("PG_DB"),
        )
    )

    SQLALCHEMY_BINDS = {
        "readonly": (
            "postgresql://{user}_readonly:{password}@{host}:{port}/{db}".format(
                user=os.environ.get("PG_USER"),
                password=os.environ.get("PG_PASSWORD"),
                host=os.environ.get("PG_HOST"),
                port=os.environ.get("PG_PORT"),
                db=os.environ.get("PG_DB"),
            )
        )
    }

    RESERVATION_SERVICE_ROOT_URL = os.environ.get(
        "RESERVATION_SERVICE_ROOT_URL"
    )
    PAYMENT_SERVICE_ROOT_URL = os.environ.get("PAYMENT_SERVICE_ROOT_URL")
    TRIP_OFFER_SERVICE_ROOT_URL = os.environ.get("TRIP_OFFER_SERVICE_ROOT_URL")

    BLUEPRINTS = [
        "src.reservation.api",
        "src.payment.api",
        "src.trip_offer.api",
    ]


class TestConfig(DefaultConfig):
    ENVIRONMENT = "test"
    TESTING = True

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://payment_test:payment_test@db:5432/payment_pg_test"
    )

    SQLALCHEMY_BINDS = {
        "readonly": "postgresql://payment_test_readonly:payment_test@db:5432/payment_pg_test"
    }
