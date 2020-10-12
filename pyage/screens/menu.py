from typing import List

from pyage.constants import KEY
from pyage.screen import Screen
from pyage.screens.items.menu_item import MenuItem


class Menu(Screen):

    _item_index: int
    _items: List[MenuItem]
    _wrap: bool

    def __init__(self, wrap: bool = False) -> None:

        super().__init__()

        self._item_index = 0
        self._items = []
        self._wrap = wrap

        self.add_key_event(key=KEY.UP, function=self.select_previous_item)
        self.add_key_event(key=KEY.DOWN, function=self.select_next_item)

    def shown(self, pushed: bool) -> None:

        super().shown(pushed)

        try:
            self._items[self._item_index].selected()
        except IndexError:
            pass

    def hidden(self, popped: bool) -> None:

        super().hidden(popped)

        try:
            self._items[self._item_index].deselected()
        except IndexError:
            pass

    def add_item(self, item: MenuItem) -> None:

        item._create(self)

        self._items.append(item)

    def select_previous_item(self, pressed: bool) -> None:

        if not pressed:
            return

        if self._item_index == 0 and not self._wrap:
            return

        self._items[self._item_index].deselected()

        self._item_index -= 1

        if self._item_index < 0:
            self._item_index = len(self._items) - 1

        self._items[self._item_index].selected()

    def select_next_item(self, pressed: bool) -> None:

        if not pressed:
            return

        if len(self._items) <= self._item_index + 1 and not self._wrap:
            return

        self._items[self._item_index].deselected()

        self._item_index += 1

        if self._item_index >= len(self._items):
            self._item_index = 0

        self._items[self._item_index].selected()
