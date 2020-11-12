from typing import Any, Callable, Dict, Tuple

from pyage.constants import EVENT
from pyage.event import Event


class ScheduleEvent(Event):

    _args: Tuple[Any, ...]
    _kwargs: Dict[str, Any]

    def __init__(
        self, function: Callable[..., None], *args: Any, **kwargs: Any
    ) -> None:

        Event.__init__(self, type=EVENT.SCHEDULE, function=function)

        self._args = args
        self._kwargs = kwargs

    def __call__(self) -> None:

        self._function(*self._args, **self._kwargs)
