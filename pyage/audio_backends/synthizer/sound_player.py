import synthizer

from pyage.sound_player import SoundPlayer


class SynthizerSoundPlayer(SoundPlayer):

    _context: synthizer.Context

    def load(self) -> None:

        self._context = synthizer.Context()

    def unload(self) -> None:

        self._context.destroy()
