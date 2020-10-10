from typing import List

import pygame

from pyage.screen import Screen
from pyage.screens.items.menu_item import MenuItem


class Menu(Screen):

    _item_index: int
    _items: List[MenuItem]

    def __init__(self) -> None:

        super().__init__()

        self._item_index = 0
        self._items = []

        self.AddKeyEvent(key=pygame.K_UP, function=self.SelectPreviousItem)
        self.AddKeyEvent(key=pygame.K_DOWN, function=self.SelectNextItem)

    def AddItem(self, item: MenuItem) -> None:

        item._create(self)

        self._items.append(item)

    def SelectPreviousItem(self, pressed: bool) -> None:

        if not pressed:
            return

        if self._item_index == 0:
            return

        self._item_index -= 1

        self._items[self._item_index].Selected()

    def SelectNextItem(self, pressed: bool) -> None:

        if not pressed:
            return

        if len(self._items) <= self._item_index + 1:
            return

        self._item_index += 1

        self._items[self._item_index].Selected()
