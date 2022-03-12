import synthizer

from pyage.assets.buffer import Buffer
from pyage.audio_backends.audio_backend import AudioBackend

from .sound_wrapper import SynthizerSoundWrapper


class Synthizer(AudioBackend):

    _context: synthizer.Context

    def __init__(self) -> None:

        synthizer.initialize()

        self._context = synthizer.Context()

    def __del__(self) -> None:

        self._context.dec_ref()

        synthizer.shutdown()

    def create_sound(self, buffer: Buffer) -> SynthizerSoundWrapper:

        return SynthizerSoundWrapper(
            buffer=buffer,
            context=self._context,
        )
