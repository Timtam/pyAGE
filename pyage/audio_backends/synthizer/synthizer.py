from typing import cast

import synthizer

from pyage.audio_backend import AudioBackend
from pyage.exceptions import AudioLoadError
from pyage.sound_buffer import SoundBuffer
from pyage.sound_player import SoundPlayer

from .sound import SynthizerSound
from .sound_buffer import SynthizerSoundBuffer
from .sound_player import SynthizerSoundPlayer


class Synthizer(AudioBackend):
    def __init__(self) -> None:

        synthizer.initialize()

    def __del__(self) -> None:

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
            player=cast(SynthizerSoundPlayer, player),
        )

    def get_sound_player(self) -> SynthizerSoundPlayer:
        return SynthizerSoundPlayer()
