from typing import Any, Callable, Optional

from pyage.assets.collection import AssetCollection
from pyage.assets.playable import Playable
from pyage.constants import KEY
from pyage.reference import Reference

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

    select_sound

        the sound to play when selecting this item. This setting overrides the
        menu's :attr:`~pyage.screens.menu.Menu.selected_sound` setting when set.

    submit_sound

        a sound to play when hitting the button.
    """

    _function: Reference[Callable[[], None]]

    submit_sound: Optional[AssetCollection[Playable]]
    """
    a sound to play when hitting the button.
    """

    def __init__(
        self,
        label: str,
        function: Callable[[], None] = lambda: None,
        select_sound: Optional[AssetCollection[Playable]] = None,
        submit_sound: Optional[AssetCollection[Playable]] = None,
    ) -> None:

        super().__init__(label=label, select_sound=select_sound)

        self._function = Reference(function)
        self.submit_sound = submit_sound

        self.add_key_event(key=KEY.RETURN, function=self.submit)

    def submit(self, pressed: bool, userdata: Any) -> None:

        snd: Optional[Playable] = None

        if not pressed:
            return

        if self.submit_sound:
            snd = self.submit_sound.get()

        if snd:
            snd.play()

        if self._function.is_alive():
            self._function()()
