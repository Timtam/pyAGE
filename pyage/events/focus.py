from typing import Callable

from pyage.constants import EVENT
from pyage.event import Event


class FocusEvent(Event):

    _gain: bool

    def __init__(self, function: Callable[[bool], None], gain: bool = False) -> None:

        Event.__init__(self, type=EVENT.FOCUS, function=function)

        self._gain = gain

    @property
    def Gain(self) -> bool:
        return self._gain
