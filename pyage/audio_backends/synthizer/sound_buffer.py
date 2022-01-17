from typing import Optional, cast

import synthizer

from pyage.sound_buffer import SoundBuffer


class SynthizerSoundBuffer(SoundBuffer):

    _buffer: Optional[synthizer.Buffer] = None

    def __init__(self, src: str) -> None:

        self._buffer = synthizer.Buffer.from_file(src)

    def __del__(self) -> None:

        if self._buffer:
            try:
                self._buffer.dec_ref()
            except synthizer.SynthizerError:
                pass

    def get_length(self) -> float:
        return cast(synthizer.Buffer, self._buffer).get_length_in_seconds()
