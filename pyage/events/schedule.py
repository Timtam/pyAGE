from typing import Any

from pyage.constants import EVENT
from pyage.event import Event
from pyage.types import ScheduleEventCallback


class ScheduleEvent(Event[ScheduleEventCallback]):

    _delay: float
    _loop: float

    def __init__(
        self,
        function: ScheduleEventCallback,
        delay: float,
        loop: float = 0.0,
        userdata: Any = None,
    ) -> None:

        super().__init__(type=EVENT.SCHEDULE, function=function, userdata=userdata)

        self._delay = delay
        self._loop = loop

    def call_callback(self, function: ScheduleEventCallback) -> None:
        function(self._userdata)

    @property
    def loop(self) -> float:
        return self._loop

    @property
    def delay(self) -> float:
        return self._delay

    def __eq__(self, other: Any) -> bool:

        if isinstance(other, ScheduleEvent):
            return (
                self._loop == other._loop
                and self._delay == other._delay
                and self._function == other._function
            )

        return NotImplemented
