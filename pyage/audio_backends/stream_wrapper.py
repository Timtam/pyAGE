from abc import ABC, abstractmethod


class StreamWrapper(ABC):
    @abstractmethod
    def play(self, restart: bool) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def pause(self) -> None:
        pass

    @property
    @abstractmethod
    def playing(self) -> bool:
        pass

    @property
    @abstractmethod
    def volume(self) -> float:
        pass

    @volume.setter
    def volume(self, value: float) -> None:
        pass
