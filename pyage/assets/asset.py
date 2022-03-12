from abc import ABC

from .buffer import Buffer


class Asset(ABC):

    _buffer: Buffer

    def __init__(self, buffer: Buffer) -> None:
        self._buffer = buffer

    @property
    def buffer(self) -> Buffer:
        return self._buffer

    def load(self) -> None:
        if self.buffer.loaded:
            return

        self.buffer.load()
