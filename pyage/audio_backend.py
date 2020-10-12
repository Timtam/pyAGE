from abc import ABC, abstractmethod

from pyage.sound_buffer import SoundBuffer


class AudioBackend(ABC):
    def load(self) -> None:
        pass

    def unload(self) -> None:
        pass

    @abstractmethod
    def create_sound_buffer(self, src: str) -> SoundBuffer:
        pass
