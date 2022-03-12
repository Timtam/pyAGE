from typing import cast

import synthizer

from pyage.assets.buffer import Buffer
from pyage.audio_backends.stream_wrapper import StreamWrapper


class SynthizerStreamWrapper(StreamWrapper):

    _buffer: synthizer.Buffer
    _context: synthizer.Context
    _generator: synthizer.BufferGenerator
    _last_position: float
    _source: synthizer.DirectSource

    def __init__(
        self,
        buffer: Buffer,
        context: synthizer.Context,
    ) -> None:

        super().__init__()

        self._context = context
        self._buffer = synthizer.Buffer.from_encoded_data(buffer.data)

        self._generator = synthizer.BufferGenerator(self._context)
        self._generator.buffer.value = self._buffer

        self._source = synthizer.DirectSource(self._context)
        self._source.add_generator(self._generator)
        self._source.pause()

        self._last_position = 0.0

    def play(self, restart: bool) -> None:

        if restart:
            self._generator.playback_position.value = 0.0
            self._last_position = 0.0

        self._source.play()

    def stop(self) -> None:

        self._source.pause()
        self._generator.playback_position.value = 0.0
        self._last_position = 0.0

    def pause(self) -> None:

        self._source.pause()
        self._last_position = self._generator.playback_position.value

    def __del__(self) -> None:

        try:
            self._source.remove_generator(self._generator)
            self._source.dec_ref()
            self._generator.dec_ref()
            self._buffer.dec_ref()
        except synthizer.SynthizerError:
            pass

    @property
    def playing(self) -> bool:

        position: float = self._generator.playback_position.value

        if position != self._last_position:
            self._last_position = position
            return True

        return False

    @property
    def volume(self) -> float:
        return cast(float, self._generator.gain.value)

    @volume.setter
    def volume(self, value: float) -> None:
        self._generator.gain.value = value
