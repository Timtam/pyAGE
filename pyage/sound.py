from abc import ABC, abstractmethod

from .sound_buffer import SoundBuffer


class Sound(ABC):

    _buffer: SoundBuffer

    def __init__(self, buffer: SoundBuffer) -> None:

        self._buffer = buffer

    @property
    def buffer(self) -> SoundBuffer:
        return self._buffer

    @abstractmethod
    def play(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def is_playing(self) -> bool:
        pass

    @property
    @abstractmethod
    def volume(self) -> float:
        pass

    @volume.setter
    def volume(self, value: float) -> None:
        # mypy seems to have an issue with abstract setters
        # so we'll avoid those for now
        raise NotImplementedError
