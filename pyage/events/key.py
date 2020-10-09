from typing import Any, Callable

from pyage.event import Event


class KeyEvent(Event):

    _key: int
    _mod: int
    _repeat: int

    def __init__(
        self,
        type: int,
        function: Callable[[bool], None],
        key: int,
        mod: int,
        repeat: int = 0,
    ) -> None:

        Event.__init__(self, type=type, function=function)

    def __eq__(self, other: Any) -> bool:

        if isinstance(other, KeyEvent):
            return (
                self.Type == other.Type
                and self.Key == other.Key
                and self.Mod == other.Mod
                and self.Function == other.Function
                and self.Repeat == other.Repeat
            )

        return False

    @property
    def Key(self) -> int:
        return self._key

    @property
    def Mod(self) -> int:
        return self._mod

    @property
    def Repeat(self) -> int:
        return self._repeat
