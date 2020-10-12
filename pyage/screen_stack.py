from typing import TYPE_CHECKING, List

from .screen import Screen

if TYPE_CHECKING:
    from pyage.app import App


class ScreenStack:

    _app: "App"
    _screen_stack: List[Screen] = []

    def __init__(self, app: "App") -> None:

        self._app = app

    def push(self, screen: Screen) -> None:

        screen._create(self._app)

        if len(self._screen_stack) > 0:
            self._screen_stack[-1].hidden(False)

        self._screen_stack.append(screen)

        screen.shown(True)

    def pop(self) -> bool:

        screen: Screen

        if len(self._screen_stack) > 0:

            screen = self._screen_stack.pop()

            screen.hidden(True)

            if len(self._screen_stack) > 0:
                self._screen_stack[-1].shown(False)

            return True

        return False

    def update(self, dt: float) -> None:

        if len(self._screen_stack) > 0:
            self._screen_stack[-1].update(dt)
