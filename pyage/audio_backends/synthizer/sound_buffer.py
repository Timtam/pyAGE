import synthizer

from pyage.sound_buffer import SoundBuffer


class SynthizerSoundBuffer(SoundBuffer):

    _buffer: synthizer.Buffer

    def __init__(self, src: str) -> None:

        self._buffer = synthizer.Buffer.from_stream("file", src)

    def __del__(self) -> None:

        self._buffer.destroy()
