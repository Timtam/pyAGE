from abc import ABC, abstractmethod


class OutputBackend(ABC):
    @abstractmethod
    def output(self, text: str, interrupt: bool = True) -> None:
        pass
