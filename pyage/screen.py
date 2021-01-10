from abc import ABC
from typing import Callable, List

import pyage.app

from .constants import KEY, MOD
from .event_processor import EventProcessor
from .events.key import KeyEvent
from .sound_player import SoundPlayer


class Screen(ABC):
    """
    This class is an abstract class and cannot be instantiated, but needs to
    be inherited to create your own screens which will then be managed by the
    :class:`pyage.screen_stack.ScreenStack` class. It also is the base class
    for any pre-defined screens within pyAGE itself.
    """

    _event_processor: EventProcessor = EventProcessor()
    _keys: List[KeyEvent]
    _sound_player: SoundPlayer

    def __init__(self) -> None:

        self._keys = []
        self._sound_player = pyage.app.App().sound_bank.create_sound_player()

    def add_key_event(
        self,
        function: Callable[[bool], None],
        key: KEY,
        mod: MOD = MOD.NONE,
        repeat: float = 0.0,
    ) -> None:
        """
        This function allows you to register keystrokes to this screen. Unlike
        :meth:`pyage.event_processor.EventProcessor.add_key_event`, the key
        events registered with this method will automatically be unregistered
        as soon as the screen is not the top-most screen on the screen stack
        anymore and will be registered again as soon as the screen gets shown
        again. Any parameters work similarly to
        :meth:`pyage.event_processor.EventProcessor.add_key_event` however.

        Parameters
        ----------
        function

            a function that receives :obj:`True` when the key was pressed or :obj:`False` if it was released

        key

            one of the several constants from the :class:`pyage.constants.KEY` enumeration

        mod

            one of :class:`pyage.constants.MOD` constants (default :attr:`pyage.constants.MOD.NONE`)

        repeat

            allows to specify a time interval in seconds after which the
            callback will be called again if the key is still pressed. Can for
            example be used to take one step for every 0.2 seconds that passed
            while the key is hold down. Default is 0, which will only raise
            the event when the key gets pressed and released.
        """

        e: KeyEvent = KeyEvent(key=key, function=function, mod=mod, repeat=repeat)

        if e not in self._keys:
            self._keys.append(e)

    def shown(self, pushed: bool) -> None:
        """
        this function is called automatically whenever the screen is shown,
        either by pushing it on top of the screen stack with the
        :meth:`pyage.screen_stack.ScreenStack.push` method, or by popping a
        screen via the :meth:`pyage.screen_stack.ScreenStack.pop` method.

        Parameters
        ----------
        pushed

            indicates if the screen was just pushed (:obj:`True`) or if it
            was shown due to another screen being popped from the stack
            (:obj:`False`).
        """

        e: KeyEvent

        for e in self._keys:
            self._event_processor.add_key_event(
                key=e._key,
                function=e._function,
                mod=e._mod,
                repeat=e._repeat,
            )

    def hidden(self, popped: bool) -> None:
        """
        this method is called whenever a screen is hidden, either because it
        was popped via :meth:`pyage.screen_stack.ScreenStack.pop` or another
        screen was pushed on top of it via
        :meth:`pyage.screen_stack.ScreenStack.push`.

        Parameters
        ----------
        popped

            indicates wether the screen was popped from the screen stack
            (:obj:`True`) or another screen was pushed on top of it
            (:obj:`False`).
        """

        e: KeyEvent

        for e in self._keys:
            self._event_processor.remove_key_event(key=e._key, mod=e._mod)

    def update(self, dt: float) -> None:
        """
        this method is called once per frame as long as the screen is the
        top-most (active) screen on the screen stack.

        Parameters
        ----------
        dt

            the delta time since the last frame of the application in seconds.
        """

        pass

    @property
    def sound_player(self) -> SoundPlayer:
        """
        A pre-configured :class:`pyage.sound_player.SoundPlayer` is provided
        for every screen created and can be used to play sounds when necessary.
        This player will automatically be cleaned up when the screen gets
        garbage-collected.
        """

        return self._sound_player

    def __del__(self) -> None:

        del self._sound_player
