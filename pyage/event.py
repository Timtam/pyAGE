from abc import ABC
from typing import Any, Callable

from pyage.constants import EVENT


class Event(ABC):

    _function: Any  # not yet supported by mypy
    _type: EVENT

    def __init__(self, type: EVENT, function: Callable[..., None]) -> None:
        self._function = function
        self._type = type

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Event):
            return self._type == other._type and self._function == other._function
        return False

    @property
    def function(self) -> Any:
        return self._function

    @property
    def type(self) -> EVENT:
        return self._type
