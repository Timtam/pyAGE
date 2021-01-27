from abc import ABC
from typing import TYPE_CHECKING, List, Optional, cast

import pyage.app
import pyage.sound_bank

from .sound import Sound
from .sound_buffer import SoundBuffer

if TYPE_CHECKING:
    from .audio_backend import AudioBackend


class SoundPlayer(ABC):

    _sounds: List[Sound]

    def __init__(self) -> None:

        self._sounds = []

    def get(self, snd: str) -> Optional[Sound]:

        app: pyage.app.App = pyage.app.App()
        bank: pyage.sound_bank.SoundBank = pyage.sound_bank.SoundBank()

        if snd not in bank:
            return None

        buffer: SoundBuffer = bank[snd]

        sound: Sound = cast("AudioBackend", app._audio_backend).create_sound(
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
