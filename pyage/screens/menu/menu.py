from typing import Any, List, Optional, Sequence, cast

from pyage.assets.collection import AssetCollection
from pyage.assets.sound import Sound
from pyage.constants import KEY
from pyage.screens.screen import Screen

from .menu_item import MenuItem


class Menu(Screen):
    """
    this class provides basic menu support for audio games. You can use it in
    two ways:

    * instantiating it and adding items to it on-the-fly (see either
      :meth:`~pyage.screens.menu.Menu.add_item` or the parameters below),
      which can be useful for displaying static data
    * inheriting it, which is encouraged for more complex applications.

    **pyAGE** already contains several types of menu items which can be
    combined freely to create whatever menu you want. All of those are
    documented here:

    Parameters
    ----------
    items

        a sequence of items for the menu. Items can however be added later
        with the use of the :meth:`~pyage.screens.menu.Menu.add_item` method.

    wrap

        does the menu wrap (pressing up or down arrow when on the edge of
        the menu will reset the cursor to the opposite end of the menu)?

    select_sound

        a sound to play when selecting an item. This is overriden by the
        selected item's :attr:`~pyage.screens.menu.MenuItem.select_sound`
        attribute.

    pan

        pan the select_sound according to the position in the menu?
    """

    _item_index: int
    _items: List[MenuItem]

    select_sound: Optional[AssetCollection[Sound]]
    """
    a sound to play when selecting an item. This is overriden by the
    selected item's :attr:`~pyage.screens.menu.MenuItem.select_sound`
    attribute.
    """

    wrap: bool
    """
    does the menu wrap (pressing up or down arrow when on the edge of
    the menu will reset the cursor to the opposite end of the menu)?
    """

    pan: bool
    """
    pan the select_sound according to the position in the menu?
    """

    def __init__(
        self,
        items: Sequence[MenuItem] = [],
        wrap: bool = False,
        select_sound: Optional[AssetCollection[Sound]] = None,
        pan: bool = False,
    ) -> None:

        super().__init__()

        self._item_index = 0
        self._items = list(items)
        self.pan = pan
        self.select_sound = select_sound
        self.wrap = wrap

        self.add_key_event(key=KEY.UP, function=self.select_previous_item)
        self.add_key_event(key=KEY.DOWN, function=self.select_next_item)

    def shown(self, pushed: bool) -> None:

        super().shown(pushed)

        try:
            self._items[self._item_index].select()
        except IndexError:
            pass

    def hidden(self, popped: bool) -> None:

        super().hidden(popped)

        try:
            self._items[self._item_index].deselect()
        except IndexError:
            pass

    def add_item(self, item: MenuItem) -> None:
        """
        adds an item to the list of items shown in this menu.

        Parameters
        ----------
        item

            the menu item (a list can be found here as well)
        """

        self._items.append(item)

    def select_previous_item(self, pressed: bool, userdata: Any) -> None:

        snd: Optional[Sound] = None

        if not pressed:
            return

        if self._item_index == 0 and not self.wrap:
            return

        self._items[self._item_index].deselect()

        self._item_index -= 1

        if self._item_index < 0:
            self._item_index = len(self._items) - 1

        if self._items[self._item_index].select_sound:
            snd = cast(
                AssetCollection[Sound], self._items[self._item_index].select_sound
            ).get()
        elif self.select_sound:
            snd = self.select_sound.get()

        if snd:
            if self.pan:
                snd.pan = self.get_item_pan_position(self._item_index, len(self._items))
            else:
                snd.pan = 0.0
            snd.play()

        self._items[self._item_index].select()

    def select_next_item(self, pressed: bool, userdata: Any) -> None:

        snd: Optional[Sound] = None

        if not pressed:
            return

        if len(self._items) <= self._item_index + 1 and not self.wrap:
            return

        self._items[self._item_index].deselect()

        self._item_index += 1

        if self._item_index >= len(self._items):
            self._item_index = 0

        if self._items[self._item_index].select_sound:
            snd = cast(
                AssetCollection[Sound], self._items[self._item_index].select_sound
            ).get()
        elif self.select_sound:
            snd = self.select_sound.get()

        if snd:
            if self.pan:
                snd.pan = self.get_item_pan_position(self._item_index, len(self._items))
            else:
                snd.pan = 0.0
            snd.play()

        self._items[self._item_index].select()

    @staticmethod
    def get_item_pan_position(item_index: int, item_count: int) -> float:

        pos: List[float]

        if item_count == 1:
            pos = [0]
        elif item_count == 2:
            pos = [-0.2, 0.2]
        elif item_count == 3:
            pos = [-0.4, 0, 0.4]
        elif item_count == 4:
            pos = [-0.6, -0.2, 0.2, 0.6]
        elif item_count == 5:
            pos = [-1.0, -0.5, 0, 0.5, 1.0]
        elif item_count > 5:
            pos = [(-1.0 + (2.0 / (item_count - 1)) * i) for i in range(item_count)]

        return pos[item_index]
