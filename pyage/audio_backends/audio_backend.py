from abc import ABC, abstractmethod

from pyage.assets.buffer import Buffer

from .sound_wrapper import SoundWrapper


class AudioBackend(ABC):
    @abstractmethod
    def create_sound(self, buffer: Buffer) -> SoundWrapper:
        pass
