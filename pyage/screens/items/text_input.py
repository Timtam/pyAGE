from typing import Any, Optional

from pyage.assets.collection import AssetCollection
from pyage.assets.playable import Playable
from pyage.constants import KEY
from pyage.event_processor import EventProcessor
from pyage.output import output

from .menu_item import MenuItem


class TextInput(MenuItem):
    """
    This class can be used to provide simple input fields (one-lined) within
    menus. You can always access the text currently available through the
    :attr:`~pyage.screens.items.text_input.TextInput.text` attribute.

    Parameters
    ----------
    label

        the text to read when selecting this item

    text

        the pre-filled text for this input field

    select_sound

        the sound to play when selecting this item. This setting overrides the
        menu's :attr:`~pyage.screens.menu.Menu.selected_sound` setting when set.
    """

    _cursor: int
    text: str
    """
    the text written to the input field
    """

    def __init__(
        self,
        label: str,
        text: str = "",
        select_sound: Optional[AssetCollection[Playable]] = None,
    ) -> None:

        super().__init__(label=label, select_sound=select_sound)

        self.text = text
        self.cursor = 0

        self.add_key_event(key=KEY.BACKSPACE, function=self.deleteBack)
        self.add_key_event(key=KEY.LEFT, function=self.cursorLeft)
        self.add_key_event(key=KEY.RIGHT, function=self.cursorRight)
        self.add_key_event(key=KEY.DELETE, function=self.deleteCurrent)

    def select(self) -> None:

        super().select()

        ev: EventProcessor = EventProcessor()

        ev.add_text_event(self.receiveText)

    def deselect(self) -> None:

        super().deselect()

        ev: EventProcessor = EventProcessor()

        ev.remove_text_event(self.receiveText)

    def receiveText(self, text: str, userdata: Any) -> None:

        self.text = self.text[: self.cursor] + text + self.text[self.cursor :]
        self.cursor += len(text)
        output(text)

    def deleteBack(self, pressed: bool, userdata: Any) -> None:

        if not pressed or self.cursor == 0:
            return

        output(self.text[self.cursor - 1])
        self.text = self.text[: (self.cursor - 1)] + self.text[self.cursor :]
        self.cursor -= 1

    def deleteCurrent(self, pressed: bool, userdata: Any) -> None:

        if not pressed or len(self.text) == self.cursor:
            return

        self.text = self.text[: self.cursor] + self.text[(self.cursor + 1) :]

        if self.cursor < len(self.text):
            output(self.text[self.cursor])
        else:
            output("empty")

    def cursorLeft(self, pressed: bool, userdata: Any) -> None:

        if not pressed or self.cursor == 0:
            return

        self.cursor -= 1
        output(self.text[self.cursor])

    def cursorRight(self, pressed: bool, userdata: Any) -> None:

        if not pressed or self.cursor == len(self.text):
            return

        self.cursor += 1

        if self.cursor < len(self.text):
            output(self.text[self.cursor])
        else:
            output("empty")

    @property
    def cursor(self) -> int:
        """
        current cursor position

        Raises
        ------
        :exc:`ValueError`

            the cursor position is out of range (text is too short)
        """

        return self._cursor

    @cursor.setter
    def cursor(self, value: int) -> None:

        if value < 0 or value > len(self.text):
            raise ValueError(
                f"text is only {len(self.text)} characters long, cursor position {value} out of range"
            )

        self._cursor = value

    def announce(self) -> None:

        output(f"{self.label} {self.text}")
