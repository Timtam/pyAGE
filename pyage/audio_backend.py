from abc import ABC, abstractmethod


class AudioBackend(ABC):
    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def unload(self) -> None:
        pass
