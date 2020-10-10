from abc import ABC
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from pyage.app import App  # noqa: F401


class Screen(ABC):

    _app: Optional["App"] = None

    def _create(self, app: "App") -> None:
        self._app = app

    @property
    def App(self) -> Optional["App"]:  # noqa: F811
        return self._app

    def Shown(self, pushed: bool) -> None:
        pass

    def Hidden(self, popped: bool) -> None:
        pass

    def Update(self, dt: float) -> None:
        pass
