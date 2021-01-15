from typing import Callable

from pyage.constants import EVENT
from pyage.event import Event


class FocusEvent(Event):

    gain: bool

    def __init__(self, function: Callable[[bool], None], gain: bool = False) -> None:

        super().__init__(type=EVENT.FOCUS, function=function)

        self.gain = gain

    def __call__(self) -> None:

        self._function(self.gain)
