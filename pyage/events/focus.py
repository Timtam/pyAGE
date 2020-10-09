from typing import Callable

from pyage.constants import EVENT
from pyage.event import Event


class FocusEvent(Event):
    def __init__(self, function: Callable[[bool], None]) -> None:

        Event.__init__(self, type=EVENT.FOCUS, function=function)
