from abc import ABC, abstractmethod

from .sound_buffer import SoundBuffer
from .sound_player import SoundPlayer


class Sound(ABC):

    _buffer: SoundBuffer
    _player: SoundPlayer

    def __init__(self, buffer: SoundBuffer, player: SoundPlayer) -> None:

        self._buffer = buffer
        self._player = player

    @property
    def buffer(self) -> SoundBuffer:
        return self._buffer

    @property
    def player(self) -> SoundPlayer:
        return self._player

    @abstractmethod
    def play(self) -> None:
        pass

    @abstractmethod
    def pause(self) -> None:
        pass
