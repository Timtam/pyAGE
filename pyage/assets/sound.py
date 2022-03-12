from typing import TYPE_CHECKING, cast

import pyage.app
from pyage.audio_backends.sound_wrapper import SoundWrapper

from .playable import Playable

if TYPE_CHECKING:
    from pyage.audio_backends.audio_backend import AudioBackend


class Sound(Playable):

    _sound: SoundWrapper

    def load(self) -> None:

        super().load()

        self._sound = cast("AudioBackend", pyage.app.App().audio_backend).create_sound(
            self.buffer
        )

    def play(self) -> None:

        self._sound.play()

    def stop(self) -> None:

        self._sound.stop()

    @property
    def playing(self) -> bool:

        return self._sound.playing

    @property
    def volume(self) -> float:
        return self._sound.volume

    @volume.setter
    def volume(self, value: float) -> None:
        self._sound.volume = value
