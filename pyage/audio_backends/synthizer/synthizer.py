import synthizer

from pyage.audio_backend import AudioBackend
from pyage.exceptions import AudioLoadException

from .sound_buffer import SynthizerSoundBuffer


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
            raise AudioLoadException(str(exc))
