import synthizer

from pyage.assets.buffer import Buffer
from pyage.audio_backends.sound_wrapper import SoundWrapper


class SynthizerSoundWrapper(SoundWrapper):

    _buffer: synthizer.Buffer
    _context: synthizer.Context
    _generator: synthizer.BufferGenerator
    _last_position: float
    _length: float
    _looping: bool
    _pan: float
    _source: synthizer.ScalarPannedSource

    def __init__(
        self,
        buffer: Buffer,
        context: synthizer.Context,
    ) -> None:

        super().__init__()

        self._context = context
        self._buffer = synthizer.Buffer.from_encoded_data(buffer.data)

        self._generator = synthizer.BufferGenerator(self._context)
        self._generator.buffer.value = self._buffer

        self._source = synthizer.ScalarPannedSource(self._context)
        self._source.add_generator(self._generator)
        self._source.pause()

        self._last_position = 0.0
        self._length = -1
        self._looping = False
        self._pan = 0.0

    def play(self) -> None:

        self._generator.playback_position.value = 0.0
        self._source.play()
        self._last_position = 0.0

    def stop(self) -> None:

        self._source.pause()

    def __del__(self) -> None:

        try:
            self._source.remove_generator(self._generator)
            self._source.dec_ref()
            self._generator.dec_ref()
            self._buffer.dec_ref()
        except synthizer.SynthizerError:
            pass

    @property
    def playing(self) -> bool:

        position: float = self._generator.playback_position.value

        if position != self._last_position:
            self._last_position = position
            return True

        return False

    @property
    def volume(self) -> float:
        return self._generator.gain.value

    @volume.setter
    def volume(self, value: float) -> None:
        self._generator.gain.value = value

    @property
    def looping(self) -> bool:
        return self._looping

    @looping.setter
    def looping(self, looping: bool) -> None:
        self._looping = looping
        self._generator.looping.value = looping

    @property
    def position(self) -> float:
        self._last_position = self._generator.playback_position.value
        return self._last_position

    @position.setter
    def position(self, position: float) -> None:
        self._last_position = position
        self._generator.playback_position.value = self._last_position

    @property
    def length(self) -> float:

        if self._length < 0:
            self._length = self._buffer.get_length_in_seconds()

        return self._length

    @property
    def pan(self) -> float:
        return self._pan

    @pan.setter
    def pan(self, value: float) -> None:
        self._pan = value
        self._source.panning_scalar.value = value
