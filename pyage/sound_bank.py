import fnmatch
import random
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Generator, List, Optional, Union, cast

from .audio_backend import AudioBackend
from .exceptions import AudioLoadError
from .sound_buffer import SoundBuffer
from .sound_player import SoundPlayer

if TYPE_CHECKING:
    from pyage.app import App


class SoundBank:

    _app: "App"
    _buffers: Dict[str, SoundBuffer]
    _file_extension: str = ".ogg"
    _source_path: Path

    def __init__(self, app: "App") -> None:

        self._app = app
        self._buffers = {}
        self._source_path = Path(".").resolve()

    @property
    def source_path(self) -> Path:
        return self._source_path

    @source_path.setter
    def source_path(self, path: Union[str, Path]) -> None:

        temp: Path

        if len(self._buffers) > 0:
            raise AttributeError(
                "the source path cannot be modified when sounds are already loaded"
            )

        if isinstance(path, str):
            temp = Path(path)
        elif isinstance(path, Path):
            temp = path
        else:
            raise TypeError("path attribute must be of type 'str'")

        if not temp.exists():
            raise AttributeError("the given path doesn't exist")

        if not temp.is_dir():
            raise AttributeError("the given path doesn't point to a directory")

        self._source_path = temp

    @property
    def file_extension(self) -> str:
        return self._file_extension

    @file_extension.setter
    def file_extension(self, extension: str) -> None:

        if not isinstance(extension, str):
            raise TypeError("extension attribute must be of type 'str'")

        if len(self._buffers) > 0:
            raise AttributeError(
                "the file extension cannot be modified when sounds are already loaded"
            )

        self._file_extension = extension

    def load(self, snd: str) -> int:

        buffer: SoundBuffer
        exc: AudioLoadError
        p: Path
        loaded: int = 0

        found: Generator[Path, None, None] = self._source_path.glob(
            snd + self._file_extension
        )

        for p in found:

            if not p.is_file():
                continue

            try:

                buffer = cast(
                    AudioBackend, self._app._audio_backend
                ).create_sound_buffer(str(p.resolve()))

                self._buffers[str(p.resolve())] = buffer

                loaded += 1

            except AudioLoadError as exc:
                warnings.warn(
                    f"unable to load audio file '{str(p.resolve())}': {str(exc)}"
                )

        return loaded

    def __contains__(self, snd: str) -> bool:

        if not isinstance(snd, str):
            return False

        name: str = str((self._source_path / (snd + self._file_extension)).resolve())

        found: List[str] = fnmatch.filter(self._buffers.keys(), name)

        if len(found) > 0:
            return True

        return False

    def unload_all(self) -> None:

        self._buffers.clear()

    def create_sound_player(self) -> SoundPlayer:

        return SoundPlayer(self._app)

    def get(self, snd: str) -> Optional[SoundBuffer]:

        if snd in self:

            name: str = str(
                (self._source_path / (snd + self._file_extension)).resolve()
            )

            found: List[str] = fnmatch.filter(self._buffers.keys(), name)

            return self._buffers[random.choice(found)]

        return None

    def __getitem__(self, snd: str) -> SoundBuffer:

        buffer: Optional[SoundBuffer] = self.get(snd)

        if buffer is None:
            raise KeyError(snd)

        return cast(SoundBuffer, buffer)
