from typing import cast

import synthizer

from pyage.sound import Sound

from .sound_buffer import SynthizerSoundBuffer
from .sound_player import SynthizerSoundPlayer


class SynthizerSound(Sound):

    _generator: synthizer.BufferGenerator
    _playing: bool
    _source: synthizer.Source3D

    def __init__(
        self, buffer: SynthizerSoundBuffer, player: SynthizerSoundPlayer
    ) -> None:

        super().__init__(buffer=buffer, player=player)

        self._generator = synthizer.BufferGenerator(
            cast(SynthizerSoundPlayer, self._player)._context
        )
        self._generator.buffer = cast(SynthizerSoundBuffer, self._buffer)._buffer

        self._source = synthizer.Source3D(
            cast(SynthizerSoundPlayer, self._player)._context
        )

        self._playing = False

    def play(self) -> None:

        if not self._playing:
            self._source.add_generator(self._generator)
            self._playing = True

    def pause(self) -> None:

        if self._playing:
            self._source.remove_generator(self._generator)
            self._playing = False
