from abc import ABC
from typing import TYPE_CHECKING, Callable, List, Optional, cast

from .constants import KEY, MOD
from .events.key import KeyEvent
from .sound_player import SoundPlayer

if TYPE_CHECKING:
    from pyage.app import App


class Screen(ABC):

    _app: "App"
    _keys: List[KeyEvent]
    _sound_player: SoundPlayer

    def __init__(self) -> None:

        from pyage.app import App

        self._app = App()
        self._keys = []
        self._sound_player = self._app.sound_bank.create_sound_player()

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
                key=e._key,
                function=e._function,
                mod=e._mod,
                repeat=e._repeat,
            )

    def hidden(self, popped: bool) -> None:

        e: KeyEvent

        for e in self._keys:
            cast("App", self._app)._event_processor.remove_key_event(
                key=e._key, mod=e._mod
            )

    def update(self, dt: float) -> None:
        pass

    @property
    def sound_player(self) -> Optional[SoundPlayer]:
        return self._sound_player

    def __del__(self) -> None:

        del self._sound_player
