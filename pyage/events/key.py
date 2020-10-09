from typing import Any, Callable

from pyage.event import Event


class KeyEvent(Event):

    _key: int
    _mod: int
    _repeat: float

    def __init__(
        self,
        type: int,
        function: Callable[[bool], None],
        key: int,
        mod: int,
        repeat: float = 0.0,
    ) -> None:

        Event.__init__(self, type=type, function=function)

    def __eq__(self, other: Any) -> bool:

        if isinstance(other, KeyEvent):
            return (
                self._type == other._type
                and self._key == other._key
                and self._mod == other._mod
                and self._function == other._function
            )

        return False

    @property
    def Key(self) -> int:
        return self._key

    @property
    def Mod(self) -> int:
        return self._mod

    @property
    def Repeat(self) -> float:
        return self._repeat
