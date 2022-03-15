from abc import abstractmethod

from .asset import Asset


class Playable(Asset):
    @abstractmethod
    def play(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
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
        # mypy seems to have an issue with abstract setters
        # so we'll avoid those for now
        raise NotImplementedError

    @property
    @abstractmethod
    def looping(self) -> bool:
        pass

    @looping.setter
    def looping(self, looping: bool) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def position(self) -> float:
        pass

    @position.setter
    def position(self, position: float) -> None:
        raise NotImplementedError()

    @property
    @abstractmethod
    def length(self) -> float:
        pass
