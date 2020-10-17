import synthizer

from pyage.sound_player import SoundPlayer


class SynthizerSoundPlayer(SoundPlayer):

    _context: synthizer.Context

    def __init__(self) -> None:

        super().__init__()

        self._context = synthizer.Context()

    def __del__(self) -> None:

        self._context.destroy()
