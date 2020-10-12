from abc import ABC
from typing import TYPE_CHECKING, Callable, List, Optional, cast

from .constants import KEY, MOD
from .events.key import KeyEvent

if TYPE_CHECKING:
    from pyage.app import App


class Screen(ABC):

    _app: Optional["App"] = None
    _keys: List[KeyEvent]

    def __init__(self) -> None:

        self._keys = []

    def _create(self, app: "App") -> None:
        self._app = app

    def add_key_event(
        self,
        key: KEY,
        function: Callable[[bool], None],
        mod: MOD = MOD.NONE,
        repeat: float = 0.0,
    ) -> None:

        e: KeyEvent = KeyEvent(key=key, function=function, mod=mod, repeat=repeat)

        if e not in self._keys:
            self._keys.append(e)

    @property
    def app(self) -> Optional["App"]:
        return self._app

    def shown(self, pushed: bool) -> None:

        e: KeyEvent

        for e in self._keys:
            cast("App", self._app)._event_processor.add_key_event(
                key=e._key, function=e._function, mod=e._mod, repeat=e._repeat
            )

    def hidden(self, popped: bool) -> None:

        e: KeyEvent

        for e in self._keys:
            cast("App", self._app)._event_processor.remove_key_event(
                key=e._key, mod=e._mod
            )

    def update(self, dt: float) -> None:
        pass
