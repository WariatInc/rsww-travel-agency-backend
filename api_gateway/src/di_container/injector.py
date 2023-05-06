import functools
import inspect
from typing import Any, Optional

from injector import Binder, ConstructorOrClassT, Injector, Provider, inject
from injector import Module as BaseModule

__all__ = ["Module"]


class TypeHinted(Provider):
    def __init__(self, cls: Any) -> None:
        self.cls = cls
        self._wrapped = self._wrapp(cls)

    @staticmethod
    def _wrapp(cls: Any) -> ConstructorOrClassT:
        @functools.wraps(cls.__init__)
        def wrapper(*args, **kwargs) -> Any:
            return cls(*args, **kwargs)

        return inject(wrapper)

    def get(self, injector: Injector) -> object:
        return injector.call_with_injection(self._wrapped)


class Module(BaseModule):
    def __call__(self, binder: Binder) -> None:
        self.binder = binder
        super().__call__(binder)

    def bind(self, type_: Any, implementation: Optional[Any] = None) -> None:
        if not implementation:
            implementation = type_

        if inspect.isclass(implementation):
            assert issubclass(implementation, type_), (
                f"{implementation.__name__} "
                f"is not a subclass of {type.__name__}"
            )

        self.binder.bind(type_, TypeHinted(implementation))
