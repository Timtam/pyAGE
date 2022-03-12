import pathlib
from typing import Optional

from pyage.exceptions import AssetLoadError

from .buffer import Buffer


class FileBuffer(Buffer):

    _data: Optional[bytes] = None
    _path: pathlib.Path

    def __init__(self, path: pathlib.Path) -> None:

        super().__init__()

        self._path = path

        if not path.exists():
            raise AssetLoadError(f"the file could not be found: {str(path)}")

    def load(self) -> None:

        if self.loaded:
            return

        with self._path.open("rb") as f:
            self._data = f.read()

    @property
    def loaded(self) -> bool:
        return self._data is not None

    @property
    def data(self) -> Optional[bytes]:
        return self._data
