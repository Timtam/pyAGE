import synthizer

from pyage.audio_backend import AudioBackend


class Synthizer(AudioBackend):
    def Load(self) -> None:

        synthizer.initialize()

    def Unload(self) -> None:

        synthizer.shutdown()
