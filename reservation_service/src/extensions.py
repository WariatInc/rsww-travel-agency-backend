from flask_sqlalchemy import SQLAlchemy

from src.utils import extend, get_current_time


db = SQLAlchemy()


@extend(db)
class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(
        db.DateTime, default=get_current_time, name="_created"
    )
    updated_at = db.Column(
        db.DateTime,
        default=get_current_time,
        onupdate=get_current_time,
        name="_updated",
    )
