from abc import ABC
from typing import TYPE_CHECKING, Optional, cast

from .sound_buffer import SoundBuffer

if TYPE_CHECKING:
    from .app import App
    from .audio_backend import AudioBackend
    from .sound import Sound


class SoundPlayer(ABC):

    _app: "App"

    def __init__(self, app: "App") -> None:

        self._app = app

    def get(self, snd: str) -> Optional["Sound"]:

        if snd not in self._app._sound_bank:
            return None

        buffer: SoundBuffer = self._app._sound_bank[snd]

        sound: Sound = cast("AudioBackend", self._app._audio_backend).create_sound(
            buffer=buffer, player=self
        )

        return sound

    def __getitem__(self, snd: str) -> "Sound":

        sound: Optional["Sound"] = self.get(snd)

        if sound is None:

            raise KeyError(snd)

        return cast("Sound", sound)
