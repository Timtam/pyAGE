from typing import TYPE_CHECKING, List

from .screen import Screen

if TYPE_CHECKING:
    from pyage.app import App


class ScreenStack:

    _app: "App"
    _screen_stack: List[Screen] = []

    def __init__(self, app: "App") -> None:

        self._app = app

    def Push(self, screen: Screen) -> None:

        screen._create(self._app)

        if len(self._screen_stack) > 0:
            self._screen_stack[-1].Hidden(False)

        self._screen_stack.append(screen)

        screen.Shown(True)

    def Pop(self) -> None:

        screen: Screen

        if len(self._screen_stack) > 0:

            screen = self._screen_stack.pop()

            screen.Hidden(True)

            if len(self._screen_stack) > 0:
                self._screen_stack[-1].Shown(False)
            else:
                self._app.Quit()

    def Update(self, dt: float) -> None:

        if len(self._screen_stack) > 0:
            self._screen_stack[-1].Update(dt)
