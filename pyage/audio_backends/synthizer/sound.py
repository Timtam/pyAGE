from typing import cast

import synthizer

from pyage.sound import Sound

from .sound_buffer import SynthizerSoundBuffer


class SynthizerSound(Sound):

    _context: synthizer.Context
    _generator: synthizer.BufferGenerator
    _last_position: float
    _source: synthizer.Source3D

    def __init__(
        self,
        buffer: SynthizerSoundBuffer,
        context: synthizer.Context,
    ) -> None:

        super().__init__(buffer=buffer)

        self._context = context
        self._generator = synthizer.BufferGenerator(self._context)
        self._generator.buffer.value = cast(SynthizerSoundBuffer, self._buffer)._buffer

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

        try:
            self._source.remove_generator(self._generator)
            self._source.dec_ref()
            self._generator.dec_ref()
        except synthizer.SynthizerError:
            pass

    def is_playing(self) -> bool:

        position: float = self._generator.playback_position.value

        if position != self._last_position:
            self._last_position = position
            return True

        return False

    @property
    def volume(self) -> float:
        return self._generator.gain.value

    @volume.setter
    def volume(self, value: float) -> None:
        self._generator.gain.value = value
