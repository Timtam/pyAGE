from typing import Any

from pyage.constants import EVENT
from pyage.events.event import Event
from pyage.types import TextEventCallback


class TextEvent(Event[TextEventCallback]):

    text: str

    def __init__(self, function: TextEventCallback, userdata: Any = None) -> None:

        super().__init__(type=EVENT.TEXT, function=function, userdata=userdata)

    def call_callback(self, function: TextEventCallback) -> None:
        function(self.text, self._userdata)
