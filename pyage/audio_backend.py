from abc import ABC, abstractmethod

from .sound import Sound
from .sound_buffer import SoundBuffer


class AudioBackend(ABC):
    @abstractmethod
    def create_sound_buffer(self, src: str) -> SoundBuffer:
        pass

    @abstractmethod
    def create_sound(self, buffer: SoundBuffer) -> Sound:
        pass
