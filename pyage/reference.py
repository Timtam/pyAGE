import weakref
from types import MethodType
from typing import Any, Callable, Generic, TypeVar, Union, cast

T = TypeVar("T", bound=Callable[..., Any])


class Reference(Generic[T]):

    _reference: Union["weakref.WeakMethod[T]", T]

    def __init__(self, referenceable: T):

        # Callable[..., Any] can be various things, unbound methods, functions,
        # lambdas, bound methods etc.
        # this reference should store all bound methods as weak references and
        # everything else as normal reference

        if isinstance(referenceable, MethodType):
            self._reference = weakref.WeakMethod(cast(T, referenceable))
        else:
            self._reference = referenceable

    def is_alive(self) -> bool:

        if isinstance(self._reference, weakref.WeakMethod):
            return self._reference() is not None
        else:
            return True

    def __call__(self) -> T:

        if isinstance(self._reference, weakref.WeakMethod):
            return cast(T, self._reference())
        else:
            return self._reference
