from abc import ABC, abstractmethod


class AudioBackend(ABC):
    @abstractmethod
    def Load(self) -> None:
        pass

    @abstractmethod
    def Unload(self) -> None:
        pass
