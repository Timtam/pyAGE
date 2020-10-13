from typing import Type, cast

import synthizer

from pyage.audio_backend import AudioBackend
from pyage.exceptions import AudioLoadError
from pyage.sound_buffer import SoundBuffer
from pyage.sound_player import SoundPlayer

from .sound import SynthizerSound
from .sound_buffer import SynthizerSoundBuffer
from .sound_player import SynthizerSoundPlayer


class Synthizer(AudioBackend):
    def load(self) -> None:

        synthizer.initialize()

    def unload(self) -> None:

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

    def get_sound_player(self) -> Type[SynthizerSoundPlayer]:
        return SynthizerSoundPlayer
