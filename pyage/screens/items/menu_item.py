from abc import ABC
from typing import Any, List, Optional, cast

from pyage.assets.collection import AssetCollection
from pyage.assets.playable import Playable
from pyage.constants import KEY, MOD
from pyage.event_processor import EventProcessor
from pyage.events.key import KeyEvent
from pyage.output import output
from pyage.types import KeyEventCallback


class MenuItem(ABC):
    """
    This is an abstract class which represents the base of every other menu
    item that can be used together with the :class:`pyage.screens.menu.Menu`
    screen. You'll need to inherit this class when creating your own type of
    menu items.

    Parameters
    ----------
    label

        the text to read when selecting this item

    select_sound

        the sound to play when selecting this item. This setting overrides the
        menu's :attr:`~pyage.screens.menu.Menu.select_sound` setting when set.
    """

    _keys: List[KeyEvent]

    label: str
    """
    the text to read when selecting this item
    """

    select_sound: Optional[AssetCollection[Playable]]
    """
    the sound to play when selecting this item. This setting overrides the
    menu's :attr:`~pyage.screens.menu.Menu.select_sound` setting when set.
    """

    def __init__(
        self, label: str, select_sound: Optional[AssetCollection[Playable]] = None
    ) -> None:

        self._keys = []
        self.label = label
        self.select_sound = select_sound

    def add_key_event(
        self,
        key: KEY,
        function: KeyEventCallback,
        mod: MOD = MOD.NONE,
        repeat: float = 0.0,
        userdata: Any = None,
    ) -> None:
        """
        Just like :meth:`pyage.screen.Screen.add_key_event`, this method allows you to add key events which will only trigger as long as this specific menu item is currently selected.

        Parameters
        ----------
        function

            a function that receives :obj:`True` when the key was pressed or
            :obj:`False` if it was released as first parameter, and the
            userdata as second parameter.

        key

            one of the several constants from the :class:`pyage.constants.KEY` enumeration

        mod

            one of :class:`pyage.constants.MOD` constants (default :attr:`pyage.constants.MOD.NONE`)

        repeat

            allows to specify a time interval in seconds after which the
            callback will be called again if the key is still pressed. Can for
            example be used to take one step for every 0.2 seconds that passed
            while the key is hold down. Default is 0, which will only raise
            the event when the key gets pressed and released.

        userdata

            userdata which will be passed to the callback
        """

        e: KeyEvent = KeyEvent(
            key=key, function=function, mod=mod, repeat=repeat, userdata=userdata
        )

        if e not in self._keys:
            self._keys.append(e)

    def select(self) -> None:
        """
        This method will be called whenever this item gets selected.
        """

        e: KeyEvent
        ev: EventProcessor = EventProcessor()

        self.announce()

        for e in self._keys:

            if not e.function:
                continue

            ev.add_key_event(
                key=e.key,
                function=cast(KeyEventCallback, e.function),
                mod=e.mod,
                repeat=e.repeat,
                userdata=e.userdata,
            )

    def deselect(self) -> None:
        """
        This method will be called whenever this item gets deselected within the menu.
        """

        e: KeyEvent
        ev: EventProcessor = EventProcessor()

        for e in self._keys:
            ev.remove_key_event(key=e.key, mod=e.mod)

    def announce(self) -> None:
        """
        This method is responsible for speaking the announcement when
        selecting this item. It will only speak the label of the item by
        default, but it can be overridden to modify this behaviour.
        """

        output(self.label)
