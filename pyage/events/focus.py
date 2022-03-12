from typing import Any

from pyage.constants import EVENT
from pyage.events.event import Event
from pyage.types import FocusEventCallback


class FocusEvent(Event[FocusEventCallback]):

    gain: bool

    def __init__(
        self, function: FocusEventCallback, gain: bool = False, userdata: Any = None
    ) -> None:

        super().__init__(type=EVENT.FOCUS, function=function, userdata=userdata)

        self.gain = gain

    def call_callback(self, function: FocusEventCallback) -> None:
        function(self.gain, self._userdata)
