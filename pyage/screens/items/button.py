from typing import Any, Callable

from pyage.constants import KEY
from pyage.output import output

from .menu_item import MenuItem


class Button(MenuItem):

    _function: Any  # not yet supported by mypy
    _text: str

    def __init__(self, text: str, function: Callable[[], None] = lambda: None) -> None:

        super().__init__()

        self._function = function
        self._text = text

        self.add_key_event(key=KEY.RETURN, function=self.submit)

    def selected(self) -> None:

        super().selected()

        output(self._text, True)

    def submit(self, pressed: bool) -> None:

        if not pressed:
            return

        self._function()
