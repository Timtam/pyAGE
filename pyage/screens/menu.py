from typing import List

import pygame

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

        self.AddKeyEvent(key=pygame.K_UP, function=self.SelectPreviousItem)
        self.AddKeyEvent(key=pygame.K_DOWN, function=self.SelectNextItem)

    def Shown(self, pushed: bool) -> None:

        super().Shown(pushed)

        try:
            self._items[self._item_index].Selected()
        except IndexError:
            pass

    def Hidden(self, popped: bool) -> None:

        super().Hidden(popped)

        try:
            self._items[self._item_index].Deselected()
        except IndexError:
            pass

    def AddItem(self, item: MenuItem) -> None:

        item._create(self)

        self._items.append(item)

    def SelectPreviousItem(self, pressed: bool) -> None:

        if not pressed:
            return

        if self._item_index == 0 and not self._wrap:
            return

        self._items[self._item_index].Deselected()

        self._item_index -= 1

        if self._item_index < 0:
            self._item_index = len(self._items) - 1

        self._items[self._item_index].Selected()

    def SelectNextItem(self, pressed: bool) -> None:

        if not pressed:
            return

        if len(self._items) <= self._item_index + 1 and not self._wrap:
            return

        self._items[self._item_index].Deselected()

        self._item_index += 1

        if self._item_index >= len(self._items):
            self._item_index = 0

        self._items[self._item_index].Selected()
