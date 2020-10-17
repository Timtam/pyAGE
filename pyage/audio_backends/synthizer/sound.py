import warnings
from typing import cast

import synthizer

from pyage.sound import Sound
from pyage.sound_player import SoundPlayer

from .sound_buffer import SynthizerSoundBuffer


class SynthizerSound(Sound):

    _context: synthizer.Context
    _generator: synthizer.BufferGenerator
    _playing: bool
    _source: synthizer.Source3D

    def __init__(
        self,
        buffer: SynthizerSoundBuffer,
        player: SoundPlayer,
        context: synthizer.Context,
    ) -> None:

        super().__init__(buffer=buffer, player=player)

        self._context = context
        self._generator = synthizer.BufferGenerator(self._context)
        self._generator.buffer = cast(SynthizerSoundBuffer, self._buffer)._buffer

        self._source = synthizer.Source3D(self._context)

        self._playing = False

    def play(self) -> None:

        if not self._playing:
            self._source.add_generator(self._generator)
            self._playing = True

    def pause(self) -> None:

        if self._playing:
            self._source.remove_generator(self._generator)
            self._playing = False

    def __del__(self) -> None:

        try:
            self._source.destroy()
            self._generator.destroy()
        except synthizer.SynthizerError:
            warnings.warn(
                "invalid handle when garbage collecting synthizer sound. SoundPlayer object not properly unloaded before ending the pyage game loop?"
            )
