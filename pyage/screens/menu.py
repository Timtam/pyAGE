from typing import Any, List, Optional

from pyage.constants import KEY
from pyage.screen import Screen
from pyage.screens.items.menu_item import MenuItem
from pyage.sound import Sound


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
    documented :ref:`here <menu-items>`:

    Parameters
    ----------
    items

        a list of items for the menu. Items can however be added later
        with the use of the :meth:`~pyage.screens.menu.Menu.add_item` method.

    wrap

        does the menu wrap (pressing up or down arrow when on the edge of
        the menu will reset the cursor to the opposite end of the menu)?

    select_sound

        a sound to play when selecting an item. This is overriden by the
        selected item's :attr:`~pyage.screens.items.menu_item.selected_sound`
        attribute.

    Attributes
    ----------

    select_sound

        a sound to play when selecting an item. This is overriden by the
        selected item's :attr:`~pyage.screens.items.menu_item.selected_sound`
        attribute.

    wrap

        does the menu wrap (pressing up or down arrow when on the edge of
        the menu will reset the cursor to the opposite end of the menu)?
    """

    _item_index: int
    _items: List[MenuItem]

    select_sound: str
    wrap: bool

    def __init__(
        self, items: List[MenuItem] = [], wrap: bool = False, select_sound: str = ""
    ) -> None:

        super().__init__()

        self._item_index = 0
        self._items = items
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

            the menu item (a list can be found :ref:`here as well <menu-items>`)
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

        if self._items[self._item_index].select_sound != "":
            snd = self.sound_player.get(self._items[self._item_index].select_sound)
        elif self.select_sound != "":
            snd = self.sound_player.get(self.select_sound)

        if snd:
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

        if self._items[self._item_index].select_sound != "":
            snd = self.sound_player.get(self._items[self._item_index].select_sound)
        elif self.select_sound != "":
            snd = self.sound_player.get(self.select_sound)

        if snd:
            snd.play()

        self._items[self._item_index].select()
