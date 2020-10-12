from abc import ABC, abstractmethod


class OutputBackend(ABC):
    def load(self) -> None:
        pass

    def unload(self) -> None:
        pass

    @abstractmethod
    def output(self, text: str, interrupt: bool = True) -> None:
        pass
