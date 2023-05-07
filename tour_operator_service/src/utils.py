from typing import Callable


def import_from(module: str, name: str) -> Callable:
    module = __import__(module, fromlist=[name])
    return getattr(module, name)
