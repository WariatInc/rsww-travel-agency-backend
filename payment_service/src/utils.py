from datetime import datetime
from types import FunctionType
from typing import Any, Callable


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
