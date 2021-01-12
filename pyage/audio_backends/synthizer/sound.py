from typing import cast

import synthizer

from pyage.sound import Sound

from .sound_buffer import SynthizerSoundBuffer


class SynthizerSound(Sound):

    _context: synthizer.Context
    _generator: synthizer.BufferGenerator
    _last_position: float
    _playing: bool
    _source: synthizer.Source3D

    def __init__(
        self,
        buffer: SynthizerSoundBuffer,
        context: synthizer.Context,
    ) -> None:

        super().__init__(buffer=buffer)

        self._context = context
        self._generator = synthizer.BufferGenerator(self._context)
        self._generator.buffer = cast(SynthizerSoundBuffer, self._buffer)._buffer

        self._source = synthizer.Source3D(self._context)

        self._last_position = 0.0
        self._playing = False

    def play(self) -> None:

        if not self._playing:
            self._source.add_generator(self._generator)
            self._last_position = self._generator.position
            self._playing = True

    def stop(self) -> None:

        if self._playing:
            self._source.remove_generator(self._generator)
            self._playing = False

    def __del__(self) -> None:

        try:
            self._source.destroy()
            self._generator.destroy()
        except synthizer.SynthizerError:
            pass

    def is_playing(self) -> bool:

        position: float = self._generator.position

        if position != self._last_position:
            self._last_position = position
            return True

        return False
