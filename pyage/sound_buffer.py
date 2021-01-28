from abc import ABC, abstractmethod


class SoundBuffer(ABC):
    @abstractmethod
    def get_length(self) -> float:
        pass
