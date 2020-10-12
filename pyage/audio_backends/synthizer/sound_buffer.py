from typing import Optional

import synthizer

from pyage.sound_buffer import SoundBuffer


class SynthizerSoundBuffer(SoundBuffer):

    _buffer: Optional[synthizer.Buffer] = None

    def __init__(self, src: str) -> None:

        self._buffer = synthizer.Buffer.from_stream("file", src)

    def __del__(self) -> None:

        if self._buffer:
            self._buffer.destroy()
