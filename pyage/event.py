from abc import ABC
from typing import Any, Callable


class Event(ABC):

    _function: Any  # not yet supported by mypy
    _type: int

    def __init__(self, type: int, function: Callable[..., None]) -> None:
        self._function = function
        self._type = type

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Event):
            return self.Type == other.Type and self.Function == other.Function
        return False

    @property
    def Function(self) -> Any:
        return self._function

    @property
    def Type(self) -> int:
        return self._type
