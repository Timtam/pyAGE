from typing import List

import pyage.app

from .screen import Screen


class ScreenStack:

    _app: "pyage.app.App"
    _screen_stack: List[Screen] = []

    def __init__(self, app: "pyage.app.App") -> None:

        self._app = app

    def push(self, screen: Screen) -> None:
        """
        This method will push a new screen on top of the screen stack.

        Parameters
        ----------
        screen

            a new screen, which will automatically receive the game focus


        Event callbacks

        - :meth:`pyage.screen.Screen.shown` will be called in the pushed
          screen to indicate that the screen was pushed onto the stack
        - :meth:`pyage.screen.Screen.hidden` will be called in the previously
          top-most screen (if available) to indicate that it is no longer shown
        """

        if len(self._screen_stack) > 0:
            self._screen_stack[-1].hidden(False)

        self._screen_stack.append(screen)

        screen.shown(True)

    def pop(self) -> bool:
        """
        Removes the top-most screen from the stack and moves focus to the next
        screen on the stack.

        Returns
        -------
        bool

            :obj:`True` if a screen was popped, :obj:`False` if there was no
            screen to be popped.


        Event callbacks

        - :meth:`pyage.screen.Screen.shown` will be called in the screen that
          is now the top-most screen on the stack to indicate that it is now
          visible again
        - :meth:`pyage.screen.Screen.hidden` will be called in the popped
          screen to indicate that its not visible anymore

        """

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
