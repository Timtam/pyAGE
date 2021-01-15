from typing import Any, Callable

from pyage.constants import KEY

from .menu_item import MenuItem


class Button(MenuItem):
    """
    This class represents a simple button which can be activated by pressing
    the return key. Doing so will call a function which can be provided by the
    user.

    Parameters
    ----------
    label

        the text to show when selecting this item

    function

        a function which gets called when pressing return while the button is
        selected.
    """

    _function: Any  # not yet supported by mypy

    def __init__(self, label: str, function: Callable[[], None] = lambda: None) -> None:

        super().__init__(label=label)

        self._function = function

        self.add_key_event(key=KEY.RETURN, function=self.submit)

    def submit(self, pressed: bool) -> None:

        if not pressed:
            return

        self._function()
