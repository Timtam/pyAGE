from typing import Any, Callable

from pyage.constants import EVENT
from pyage.event import Event


class KeyEvent(Event):

    _key: int
    _mod: int
    _pressed: bool
    _repeat: float

    def __init__(
        self,
        function: Callable[[bool], None],
        key: int,
        mod: int,
        repeat: float = 0.0,
        pressed: bool = True,
    ) -> None:

        Event.__init__(self, type=EVENT.KEY, function=function)

        self._key = key
        self._mod = mod
        self._repeat = repeat
        self._pressed = pressed

    def __eq__(self, other: Any) -> bool:

        if isinstance(other, KeyEvent):
            return (
                self._key == other._key
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

    @property
    def Pressed(self) -> bool:
        return self._pressed
