from typing import TYPE_CHECKING, Dict

from .sound_buffer import SoundBuffer

if TYPE_CHECKING:
    from pyage.app import App


class SoundBank:

    _app: "App"
    _buffers: Dict[str, SoundBuffer]

    def __init__(self, app: "App") -> None:

        self._app = app
        self._buffers = {}
