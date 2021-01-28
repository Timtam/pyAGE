from typing import Any

from pyage.constants import EVENT
from pyage.event import Event
from pyage.types import ScheduleEventCallback


class ScheduleEvent(Event[ScheduleEventCallback]):
    def __init__(self, function: ScheduleEventCallback, userdata: Any = None) -> None:

        super().__init__(type=EVENT.SCHEDULE, function=function, userdata=userdata)

    def call_callback(self, function: ScheduleEventCallback) -> None:
        function(self._userdata)
