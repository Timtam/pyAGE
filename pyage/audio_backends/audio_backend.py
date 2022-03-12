from abc import ABC, abstractmethod

from pyage.assets.buffer import Buffer

from .sound_wrapper import SoundWrapper
from .stream_wrapper import StreamWrapper


class AudioBackend(ABC):
    @abstractmethod
    def create_sound(self, buffer: Buffer) -> SoundWrapper:
        pass

    @abstractmethod
    def create_stream(self, buffer: Buffer) -> StreamWrapper:
        pass
