from abc import ABC
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from pyage.app import App  # noqa: F401
    from pyage.screens.menu import Menu  # noqa: F401


class MenuItem(ABC):

    _menu: Optional["Menu"] = None

    def __init__(self) -> None:

        pass

    def _create(self, menu: "Menu") -> None:

        self._menu = menu

    def Selected(self) -> None:

        pass

    @property
    def Menu(self) -> Optional["Menu"]:  # noqa: F811
        return self._menu
