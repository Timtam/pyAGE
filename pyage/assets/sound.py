import sys
from typing import TYPE_CHECKING, Any, Optional, cast

import pyage.app
import pyage.event_processor
from pyage.audio_backends.sound_wrapper import SoundWrapper

from .playable import Playable

if TYPE_CHECKING:
    from pyage.audio_backends.audio_backend import AudioBackend


class Sound(Playable):

    _ref: Optional["Sound"]
    _prefer_caching: bool = False
    _sound: SoundWrapper

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._ref = None

    def load(self, cached: bool) -> None:

        super().load(cached=cached)

        self._sound = cast("AudioBackend", pyage.app.App().audio_backend).create_sound(
            self.buffer
        )

        if cached is False:
            self._ref = self
            pyage.event_processor.EventProcessor().add_schedule_event(
                0.1, self._handle_caching, 0.1
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

    def _handle_caching(self, data: Any) -> None:
        if not self.playing:
            if sys.getrefcount(self) == 4:
                self._ref = None
                pyage.event_processor.EventProcessor().remove_schedule_event(
                    self._handle_caching, 0.1
                )

    @property
    def looping(self) -> bool:
        return self._sound.looping

    @looping.setter
    def looping(self, looping: bool) -> None:
        self._sound.looping = looping

    @property
    def position(self) -> float:
        return self._sound.position

    @position.setter
    def position(self, position: float) -> None:
        self._sound.position = position

    @property
    def length(self) -> float:
        return self._sound.length
