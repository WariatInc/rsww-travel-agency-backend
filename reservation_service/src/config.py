import os


class Config:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class DefaultConfig(Config):
    ENVIRONMENT = "dev"
    PROJECT = "reservation_service"
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

    SQLALCHEMY_CONNECTION_OPTIONS = {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }

    BLUEPRINTS = ["src.reservation.api"]

    TASKS = {
        "src.reservation.domain.tasks": [
            ("cancel_accepted_reservations_after_timeout", "interval", 2)
        ]
    }

    RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
    RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT")
    RABBITMQ_USER = os.environ.get("RABBITMQ_USER")
    RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD")


class ProductionConfig(DefaultConfig):
    ENVIRONMENT = "prod"
    CONSUMERS = [
        "src.reservation.infrastructure.message_broker.consumer",
        "src.payment.infrastructure.message_broker.consumer",
    ]


class TestConfig(DefaultConfig):
    ENVIRONMENT = "test"
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "postgresql://reservation_test:reservation_test@db:5432/reservation_pg_test"

    SQLALCHEMY_BINDS = {
        "readonly": "postgresql://reservation_test_readonly:reservation_test@db:5432/reservation_pg_test"
    }
