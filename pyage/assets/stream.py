from typing import TYPE_CHECKING, cast

import pyage.app
from pyage.audio_backends.stream_wrapper import StreamWrapper

from .playable import Playable

if TYPE_CHECKING:
    from pyage.audio_backends.audio_backend import AudioBackend


class Stream(Playable):

    _stream: StreamWrapper

    def load(self, cached: bool) -> None:

        super().load(cached=cached)

        self._stream = cast(
            "AudioBackend", pyage.app.App().audio_backend
        ).create_stream(self.buffer)

    def play(self, restart: bool = False) -> None:

        self._stream.play(restart)

    def stop(self) -> None:

        self._stream.stop()

    def pause(self) -> None:

        self._stream.pause()

    @property
    def playing(self) -> bool:

        return self._stream.playing

    @property
    def volume(self) -> float:
        return self._stream.volume

    @volume.setter
    def volume(self, value: float) -> None:
        self._stream.volume = value

    @property
    def looping(self) -> bool:
        return self._stream.looping

    @looping.setter
    def looping(self, looping: bool) -> None:
        self._stream.looping = looping

    @property
    def position(self) -> float:
        return self._stream.position

    @position.setter
    def position(self, position: float) -> None:
        self._stream.position = position

    @property
    def length(self) -> float:
        return self._stream.length
