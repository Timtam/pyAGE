import fnmatch
import random
import warnings
from pathlib import Path
from typing import Dict, Generator, List, Optional, Union, cast

from pysingleton import PySingleton

import pyage.app

from .audio_backend import AudioBackend
from .exceptions import AudioLoadError
from .sound_buffer import SoundBuffer
from .sound_player import SoundPlayer


class SoundBank(metaclass=PySingleton):
    """
    The sound bank allows you to load sound buffers via the
    :meth:`~pyage.sound_bank.SoundBank.load` method, after which you can access
    the loaded buffers either by indexing the sound bank object with
    :code:`app.sound_bank['test']` or by calling the
    :meth:`~pyage.sound_bank.SoundBank.get` method. Both those ways will return
    a :class:`pyage.sound_buffer.SoundBuffer` class, which will usually not be
    of any help to you, since they're mostly used internally. To access the
    playable sounds, you'll first need to create a
    :class:`pyage.sound_player.SoundPlayer` object by calling the
    :meth:`pyage.sound_bank.SoundBank.create_sound_player` method. A sound
    player is used to control the behaviour of sounds in a specific scene,
    like reverb effects, overall position etc, and will finally give you
    access to all the sounds you can play in your game. Since you cannot gain
    access to a sound player without the sound bank, you'll first have to take
    a look into the useful tools this class can offer you.
    """

    _buffers: Dict[str, SoundBuffer]
    _file_extension: str = ".ogg"
    _source_path: Path

    def __init__(self) -> None:

        self._buffers = {}
        self._source_path = Path(".").resolve()

    @property
    def source_path(self) -> Path:
        """
        the source path is the path where the
        :meth:`~pyage.sound_bank.SoundBank.load` method will look by default
        when searching for a specific sound to load. The default is the
        working directory of the current app.

        Raises
        ------
        :exc:`AttributeError`

            either you cannot change the source path after sounds are already
            loaded, the given path does not exist or the path doesn't point to
            a directory

        :exc:`TypeError`

            path parameter has invalid type
        """

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
            raise TypeError("path attribute must be a Path or str")

        if not temp.exists():
            raise AttributeError("the given path doesn't exist")

        if not temp.is_dir():
            raise AttributeError("the given path doesn't point to a directory")

        self._source_path = temp

    @property
    def file_extension(self) -> str:
        """
        the file extension that will automatically be added to the sound to be
        loaded by :meth:`~pyage.sound_bank.SoundBank.load`

        Raises
        ------
        :exc:`AttributeError`

            you cannot change the file extension when sounds are already loaded

        :exc:`TypeError`

            extension must be of type str
        """

        return self._file_extension

    @file_extension.setter
    def file_extension(self, extension: str) -> None:

        if not isinstance(extension, str):
            raise TypeError("extension attribute must be of type str")

        if len(self._buffers) > 0:
            raise AttributeError(
                "the file extension cannot be modified when sounds are already loaded"
            )

        self._file_extension = extension

    def load(self, snd: str) -> int:
        """
        loads one or more sounds into memory and prepares it to be played

        Parameters
        ----------
        snd

            a specifier which will be used to search for sounds. The specifier
            may be a file name without the
            :attr:`~pyage.sound_bank.SoundBank.source_path` path prefix and may
            not have an extension, since the
            :attr:`~pyage.sound_bank.SoundBank.file_extension` will
            automatically be appended. You can however use glob patterns to
            search for multiple files at once.

            .. code-block:: python

               # this will load all files starting with sword-hit_
               pyage.app.App().sound_bank.load('sword-hit_*')

        Returns
        -------
        int

            the amount of sounds loaded
        """

        app: pyage.app.App = pyage.app.App()
        buffer: SoundBuffer
        exc: AudioLoadError
        loaded: int = 0
        p: Path

        found: Generator[Path, None, None] = self._source_path.glob(
            snd + self._file_extension
        )

        for p in found:

            if not p.is_file():
                continue

            try:

                buffer = cast(AudioBackend, app._audio_backend).create_sound_buffer(
                    str(p.resolve())
                )

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
        """
        create a sound player which is needed to play and manage sounds
        """

        return SoundPlayer()

    def get(self, snd: str) -> Optional[SoundBuffer]:
        """
        access a sound buffer object which was previously loaded via
        :meth:`~pyage.sound_bank.SoundBank.load`. This will usually not be
        required, since all the sound buffer handling will be done for you
        automatically.

        Parameters
        ----------
        snd

            a specifier like in :meth:`pyage.sound_buffer.SoundBuffer.load`.
            If a glob pattern is used, a random sound buffer matching the
            pattern will be returned.
        """

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
