from abc import ABC
from typing import TYPE_CHECKING, Callable, List, Optional, cast

from pyage.constants import KEY, MOD
from pyage.events.key import KeyEvent

if TYPE_CHECKING:
    from pyage.app import App
    from pyage.screens.menu import Menu


class MenuItem(ABC):

    _keys: List[KeyEvent]
    _menu: Optional["Menu"] = None

    def __init__(self) -> None:

        self._keys = []

    def _create(self, menu: "Menu") -> None:

        self._menu = menu

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

    def selected(self) -> None:

        e: KeyEvent

        for e in self._keys:
            cast("App", cast("Menu", self._menu)._app)._event_processor.add_key_event(
                key=e._key, function=e._function, mod=e._mod, repeat=e._repeat
            )

    def deselected(self) -> None:

        e: KeyEvent

        for e in self._keys:
            cast(
                "App", cast("Menu", self._menu)._app
            )._event_processor.remove_key_event(key=e._key, mod=e._mod)

    @property
    def menu(self) -> Optional["Menu"]:
        return self._menu
