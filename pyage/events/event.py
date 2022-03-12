from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

from pyage.constants import EVENT
from pyage.reference import Reference

T = TypeVar("T")


class Event(Generic[T], ABC):

    _function: Reference[T]
    _type: EVENT
    _userdata: Any

    def __init__(self, type: EVENT, function: T, userdata: Any = None) -> None:
        self._function = Reference(function)
        self._type = type
        self._userdata = userdata

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Event):
            return self._type == other._type and self._function == other._function
        return NotImplemented

    def __call__(self) -> None:

        if self._function.is_alive():
            self.call_callback(self._function())

    @abstractmethod
    def call_callback(self, function: T) -> None:
        pass

    @property
    def function(self) -> Optional[T]:
        if self._function.is_alive():
            return self._function()
        else:
            return None

    @property
    def type(self) -> EVENT:
        return self._type

    @property
    def userdata(self) -> Any:
        return self._userdata
