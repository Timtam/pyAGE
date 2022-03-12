from typing import Any

from pyage.constants import EVENT, KEY, MOD
from pyage.events.event import Event
from pyage.types import KeyEventCallback


class KeyEvent(Event[KeyEventCallback]):

    _key: KEY
    _mod: MOD
    _repeat: float
    pressed: bool

    def __init__(
        self,
        function: KeyEventCallback,
        key: KEY,
        mod: MOD,
        repeat: float = 0.0,
        pressed: bool = True,
        userdata: Any = None,
    ) -> None:

        super().__init__(type=EVENT.KEY, function=function, userdata=userdata)

        self._key = key
        self._mod = mod
        self._repeat = repeat
        self.pressed = pressed

    def __eq__(self, other: Any) -> bool:

        if isinstance(other, KeyEvent):
            return (
                self._key == other._key
                and self._mod == other._mod
                and self._function == other._function
            )

        return NotImplemented

    @property
    def key(self) -> KEY:
        return self._key

    @property
    def mod(self) -> MOD:
        return self._mod

    @property
    def repeat(self) -> float:
        return self._repeat

    def call_callback(self, function: KeyEventCallback) -> None:
        function(self.pressed, self._userdata)
