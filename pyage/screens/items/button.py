from typing import Any, Callable

from pyage.constants import KEY
from pyage.output import Output

from .menu_item import MenuItem


class Button(MenuItem):

    _function: Any  # not yet supported by mypy
    _text: str

    def __init__(self, text: str, function: Callable[[], None] = lambda: None) -> None:

        super().__init__()

        self._function = function
        self._text = text

        self.AddKeyEvent(key=KEY.RETURN, function=self.Submit)

    def Selected(self) -> None:

        super().Selected()

        Output(self._text, True)

    def Submit(self, pressed: bool) -> None:

        if not pressed:
            return

        self._function()
