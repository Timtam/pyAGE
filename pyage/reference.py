import weakref
from types import MethodType
from typing import Generic, TypeVar, Union, cast

T = TypeVar("T")


class Reference(Generic[T]):

    _reference: Union[weakref.WeakMethod, T]

    def __init__(self, referenceable: T):

        if isinstance(referenceable, MethodType):
            self._reference = weakref.WeakMethod(cast(MethodType, referenceable))
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
