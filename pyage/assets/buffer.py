from abc import ABC, abstractmethod
from typing import Optional


class Buffer(ABC):
    @abstractmethod
    def load(self) -> None:
        pass

    @property
    @abstractmethod
    def loaded(self) -> bool:
        pass

    @property
    @abstractmethod
    def data(self) -> Optional[bytes]:
        pass
