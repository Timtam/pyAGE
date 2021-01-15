from typing import Any, Dict, Tuple

from typing_extensions import Protocol

from pyage.constants import EVENT
from pyage.event import Event


class TextEventCallback(Protocol):
    def __call__(self, text: str, *args: Any, **kwargs: Any) -> None:
        ...


class TextEvent(Event):

    _args: Tuple[Any, ...]
    _kwargs: Dict[str, Any]
    text: str

    def __init__(self, function: TextEventCallback, *args: Any, **kwargs: Any) -> None:

        super().__init__(type=EVENT.TEXT, function=function)

        self._args = args
        self._kwargs = kwargs

    def __call__(self) -> None:

        self._function(self.text, *self._args, **self._kwargs)
