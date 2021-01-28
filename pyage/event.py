from abc import ABC
from typing import Any, Generic, TypeVar

from pyage.constants import EVENT

T = TypeVar("T")


class Event(Generic[T], ABC):

    _function: T
    _type: EVENT
    _userdata: Any

    def __init__(self, type: EVENT, function: T, userdata: Any = None) -> None:
        self._function = function
        self._type = type
        self._userdata = userdata

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Event):
            return self._type == other._type and self._function == other._function
        return NotImplemented

    def __call__(self) -> None:

        self.call_callback(self._function)

    def call_callback(self, function: T) -> None:
        pass

    @property
    def function(self) -> T:
        return self._function

    @property
    def type(self) -> EVENT:
        return self._type

    @property
    def userdata(self) -> Any:
        return self._userdata
