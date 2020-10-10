from pyage.output import Output

from .menu_item import MenuItem


class Button(MenuItem):

    _text: str

    def __init__(self, text: str) -> None:

        super().__init__()

        self._text = text

    def Selected(self) -> None:

        super().Selected()

        Output(self._text, True)
