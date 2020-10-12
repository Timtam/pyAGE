import synthizer

from pyage.audio_backend import AudioBackend


class Synthizer(AudioBackend):
    def load(self) -> None:

        synthizer.initialize()

    def unload(self) -> None:

        synthizer.shutdown()
