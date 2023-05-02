from datetime import datetime
from types import FunctionType
from typing import Any, Callable

import alembic
import sqlalchemy as sqla


def extend(class_to_extend: Any) -> Any:
    def decorator(class_to_extend_with: Any) -> Any:
        setattr(
            class_to_extend,
            class_to_extend_with.__name__,
            class_to_extend_with,
        )
        return class_to_extend_with

    return decorator


def get_current_time() -> datetime:
    return datetime.utcnow()


def import_from(module: str, name: str) -> Callable:
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def has_constructor_defined(cls: Any) -> bool:
    return isinstance(cls.__init__, FunctionType)


def alter_enum(table, column_name, enum_name, old_options, new_options):
    old_type = sqla.Enum(*old_options, name=enum_name)
    new_type = sqla.Enum(*new_options, name=enum_name)
    tmp_type = sqla.Enum(*new_options, name="_" + enum_name)

    # create a tmp type, convert and drop the old type
    tmp_type.create(alembic.op.get_bind(), checkfirst=False)
    alembic.op.execute(
        'ALTER TABLE "{0}" ALTER COLUMN {1} TYPE _{2} USING {1}::text::_{2}'.format(
            table, column_name, enum_name
        )
    )
    old_type.drop(alembic.op.get_bind(), checkfirst=False)

    # create and convert to the new type, drop the tmp type
    new_type.create(alembic.op.get_bind(), checkfirst=False)
    alembic.op.execute(
        'ALTER TABLE "{0}" ALTER COLUMN {1} TYPE {2} USING {1}::text::{2}'.format(
            table, column_name, enum_name
        )
    )
    tmp_type.drop(alembic.op.get_bind(), checkfirst=False)
