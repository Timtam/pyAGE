from abc import ABC, abstractmethod


class OutputBackend(ABC):
    def Load(self) -> None:
        pass

    def Unload(self) -> None:
        pass

    @abstractmethod
    def Output(self, text: str, interrupt: bool = True) -> None:
        pass
