from typing import cast

import synthizer

from pyage.assets.buffer import Buffer
from pyage.audio_backends.sound_wrapper import SoundWrapper


class SynthizerSoundWrapper(SoundWrapper):

    _buffer: synthizer.Buffer
    _context: synthizer.Context
    _generator: synthizer.BufferGenerator
    _last_position: float
    _source: synthizer.Source3D

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

        self._source = synthizer.Source3D(self._context)
        self._source.add_generator(self._generator)
        self._source.pause()

        self._last_position = 0.0

    def play(self) -> None:

        self._generator.playback_position.value = 0.0
        self._source.play()
        self._last_position = 0.0

    def stop(self) -> None:

        self._source.pause()

    def __del__(self) -> None:

        print("deleting again")
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
