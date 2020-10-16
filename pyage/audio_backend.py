from abc import ABC, abstractmethod
from typing import Type

from .sound import Sound
from .sound_buffer import SoundBuffer
from .sound_player import SoundPlayer


class AudioBackend(ABC):
    @abstractmethod
    def create_sound_buffer(self, src: str) -> SoundBuffer:
        pass

    @abstractmethod
    def create_sound(self, buffer: SoundBuffer, player: SoundPlayer) -> Sound:
        pass

    def get_sound_player(self) -> Type[SoundPlayer]:
        return SoundPlayer
