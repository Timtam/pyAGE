from abc import ABC
from typing import TYPE_CHECKING, List, Optional, cast

from .sound import Sound
from .sound_buffer import SoundBuffer

if TYPE_CHECKING:
    from .app import App
    from .audio_backend import AudioBackend


class SoundPlayer(ABC):

    _app: "App"
    _sounds: List[Sound]

    def __init__(self, app: "App") -> None:

        self._app = app
        self._sounds = []

    def get(self, snd: str) -> Optional[Sound]:

        if snd not in self._app._sound_bank:
            return None

        buffer: SoundBuffer = self._app._sound_bank[snd]

        sound: Sound = cast("AudioBackend", self._app._audio_backend).create_sound(
            buffer=buffer
        )

        self._sounds.append(sound)

        return sound

    def __getitem__(self, snd: str) -> Sound:

        sound: Optional[Sound] = self.get(snd)

        if sound is None:

            raise KeyError(snd)

        return cast(Sound, sound)

    def __del__(self) -> None:

        self._sounds.clear()
