from abc import ABC
from typing import TYPE_CHECKING, Dict, List, Optional, cast

import pyage.app
import pyage.sound_bank

from .sound import Sound
from .sound_buffer import SoundBuffer

if TYPE_CHECKING:
    from .audio_backend import AudioBackend


class SoundPlayer(ABC):

    _cache_size: int
    _sounds: Dict[str, List[Sound]]

    def __init__(self, cache_size: int) -> None:

        self._cache_size = cache_size
        self._sounds = {}

    def get(self, snd: str, cached: bool = True) -> Optional[Sound]:

        app: pyage.app.App = pyage.app.App()
        sound: Optional[Sound]

        if cached:

            if snd in self._sounds:

                try:
                    sound = next(s for s in self._sounds[snd] if not s.is_playing())
                except StopIteration:
                    sound = None

                if sound:
                    return sound

        bank: pyage.sound_bank.SoundBank = pyage.sound_bank.SoundBank()

        if snd not in bank:
            return None

        buffer: SoundBuffer = bank[snd]

        sound = cast("AudioBackend", app._audio_backend).create_sound(buffer=buffer)

        if not cached:
            return sound

        if self._cache_size > 0 and self.get_cache_size() >= self._cache_size:
            self.clean_cache()

        if self._cache_size > 0 and self.get_cache_size() >= self._cache_size:
            raise MemoryError(
                "cache size overflow. too many simultaneous sounds are playing. Consider raising the pyage.sound_bank.SoundBank.cache_size value"
            )

        if snd not in self._sounds:
            self._sounds[snd] = []

        self._sounds[snd].append(cast(Sound, sound))

        return sound

    def __getitem__(self, snd: str) -> Sound:

        sound: Optional[Sound] = self.get(snd)

        if sound is None:

            raise KeyError(snd)

        return cast(Sound, sound)

    def __del__(self) -> None:

        self._sounds.clear()

    def clean_cache(self) -> None:

        self._sounds = {
            name: [s for s in sounds if s.is_playing()]
            for (name, sounds) in self._sounds.items()
        }

    def get_cache_size(self) -> int:
        return sum([len(v) for v in self._sounds.values()])
