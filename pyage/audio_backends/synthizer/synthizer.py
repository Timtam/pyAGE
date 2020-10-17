from typing import cast

import synthizer

from pyage.audio_backend import AudioBackend
from pyage.exceptions import AudioLoadError
from pyage.sound_buffer import SoundBuffer
from pyage.sound_player import SoundPlayer

from .sound import SynthizerSound
from .sound_buffer import SynthizerSoundBuffer


class Synthizer(AudioBackend):

    _context: synthizer.Context

    def __init__(self) -> None:

        synthizer.initialize()

        self._context = synthizer.Context()

    def __del__(self) -> None:

        self._context.destroy()

        synthizer.shutdown()

    def create_sound_buffer(self, src: str) -> SynthizerSoundBuffer:

        exc: synthizer.SynthizerError

        try:
            return SynthizerSoundBuffer(src)
        except synthizer.SynthizerError as exc:
            raise AudioLoadError(str(exc))

    def create_sound(self, buffer: SoundBuffer, player: SoundPlayer) -> SynthizerSound:

        return SynthizerSound(
            buffer=cast(SynthizerSoundBuffer, buffer),
            player=player,
            context=self._context,
        )
