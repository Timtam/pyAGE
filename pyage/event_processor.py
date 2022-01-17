import copy
import heapq
import time
import traceback
from typing import Any, List, Optional, Sequence, Tuple, cast

import pygame
from pysingleton import PySingleton

from pyage.constants import EVENT, KEY, MOD
from pyage.event import Event
from pyage.events.focus import FocusEvent
from pyage.events.key import KeyEvent
from pyage.events.schedule import ScheduleEvent
from pyage.events.text import TextEvent
from pyage.types import (
    FocusEventCallback,
    KeyEventCallback,
    ScheduleEventCallback,
    TextEventCallback,
)


class EventProcessor(metaclass=PySingleton):

    _event_queue: List[Tuple[float, Event]] = []
    _registered_events: List[Event] = []
    _text_event_count: int = 0
    _unregistered_events: List[Event] = []

    def _process_pygame_event(self, e: pygame.event.Event) -> None:

        f: Optional[Event]
        r_f: Event

        if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:

            try:
                f = next(
                    r_f
                    for r_f in self._registered_events
                    if r_f.type == EVENT.KEY
                    and cast(KeyEvent, r_f).key == e.key
                    and e.mod & cast(KeyEvent, r_f).mod == cast(KeyEvent, r_f).mod
                )
            except StopIteration:
                f = None

            if f:

                r_f = copy.copy(f)
                cast(KeyEvent, r_f).pressed = (
                    True if e.type == pygame.KEYDOWN else False
                )

                heapq.heappush(
                    self._event_queue,
                    (
                        time.time(),
                        r_f,
                    ),
                )

        elif e.type == pygame.WINDOWFOCUSGAINED or e.type == pygame.WINDOWFOCUSLOST:

            for f in self._registered_events:

                if f.type == EVENT.FOCUS:

                    r_f = copy.copy(f)
                    cast(FocusEvent, r_f).gain = e.type == pygame.WINDOWFOCUSGAINED

                    heapq.heappush(
                        self._event_queue,
                        (
                            time.time(),
                            r_f,
                        ),
                    )

        elif e.type == pygame.TEXTINPUT:

            for f in self._registered_events:

                if f.type == EVENT.TEXT:

                    r_f = copy.copy(f)
                    cast(TextEvent, r_f).text = e.text

                    heapq.heappush(
                        self._event_queue,
                        (
                            time.time(),
                            r_f,
                        ),
                    )

    def _process_event(self, e: Event) -> None:

        keys: Sequence[bool]

        if e in self._unregistered_events:
            return

        if not e.function:
            return

        if e.type == EVENT.KEY:

            if cast(KeyEvent, e).pressed and cast(KeyEvent, e).repeat > 0:

                keys = pygame.key.get_pressed()

                if (
                    cast(KeyEvent, e).mod == 0 and not bool(keys[cast(KeyEvent, e).key])
                ) or (
                    cast(KeyEvent, e).mod != 0
                    and (
                        pygame.key.get_mods() & cast(KeyEvent, e).mod
                        != cast(KeyEvent, e).mod
                        or not bool(keys[cast(KeyEvent, e).key])
                    )
                ):
                    return

            if cast(KeyEvent, e).repeat > 0 and cast(KeyEvent, e).pressed:
                heapq.heappush(
                    self._event_queue,
                    (
                        time.time() + cast(KeyEvent, e).repeat,
                        e,
                    ),
                )

        e()

    def _unregister_event(self, e: Event) -> None:

        try:
            self._registered_events.remove(e)
        except ValueError:
            pass

    def process(self) -> None:

        e: pygame.event.Event
        f: Event
        events: List[pygame.event.Event]

        try:
            events = pygame.event.get()
        except pygame.error:
            events = []

        for e in events:
            if e.type != pygame.NOEVENT:
                self._process_pygame_event(e)

        if len(self._event_queue) == 0:
            return

        current_time: float = time.time()

        while len(self._event_queue) > 0 and self._event_queue[0][0] <= current_time:

            f = heapq.heappop(self._event_queue)[1]

            try:
                self._process_event(f)
            except BaseException:
                print(
                    "exception encountered and silently ignored:\n",
                    traceback.format_exc(),
                )

        if len(self._unregistered_events) == 0:
            return

        for f in self._unregistered_events:
            self._unregister_event(f)

        self._unregistered_events.clear()

    def add_key_event(
        self,
        function: KeyEventCallback,
        key: KEY,
        mod: MOD = MOD.NONE,
        repeat: float = 0.0,
        userdata: Any = None,
    ) -> None:
        """
        registers a callback which gets called whenever the specified key is pressed

        Parameters
        ----------
        function

            a function that receives :obj:`True` when the key was pressed or
            :obj:`False` if it was released as first argument, and the provided
            userdata as second parameter

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

        userdata

            data which will be passed to the registered function
        """

        self._registered_events.append(
            KeyEvent(
                function=function, key=key, mod=mod, repeat=repeat, userdata=userdata
            )
        )

    def add_focus_event(
        self, function: FocusEventCallback, userdata: Any = None
    ) -> None:
        """
        registers a callback that gets called whenever the pyAGE app loses or
        receives focus. Can be used to pause a game or silence sounds when the
        user switches to another window.

        Parameters
        ----------
        function

            a callback that will receive :obj:`True` as argument when the app
            receives focus or :obj:`False` when it loses focus as first
            parameter, and the userdata as second parameter.

        userdata

            userdata which will be passed to the callback
        """

        self._registered_events.append(FocusEvent(function=function, userdata=userdata))

    def remove_key_event(self, key: KEY, mod: MOD = MOD.NONE) -> None:
        """
        removes a previously registered callback to no longer get called
        whenever the key is pressed.

        Parameters
        ----------
        key

            one of the :class:`pyage.constants.KEY` constants

        mod

            one of the :class:`pyage.constants.MOD` constants (default
            :attr:`pyage.constants.MOD.NONE`)
        """

        f: Event

        for f in self._registered_events:
            if (
                f not in self._unregistered_events
                and f.type == EVENT.KEY
                and cast(KeyEvent, f)._key == key
                and cast(KeyEvent, f)._mod == mod
            ):
                self._unregistered_events.append(f)

    def remove_focus_event(self, function: FocusEventCallback) -> None:
        """
        removes a previously registered focus callback

        Parameters
        ----------
        function

            the function registered via
            :meth:`~pyage.event_processor.EventProcessor.add_focus_event`
        """

        f: Event

        for f in self._registered_events:
            if (
                f not in self._unregistered_events
                and f.type == EVENT.FOCUS
                and f.function == function
            ):
                self._unregistered_events.append(f)

    def add_schedule_event(
        self, delay: float, function: ScheduleEventCallback, userdata: Any = None
    ) -> None:
        """
        registers a callback that gets called after a given period of time

        Parameters
        ----------
        delay

            a certain time in seconds

        function

            a callback accepting only the userdata as parameter.

        userdata

            userdata which will be passed to the callback
        """

        heapq.heappush(
            self._event_queue,
            (time.time() + delay, ScheduleEvent(function=function, userdata=userdata)),
        )

    def add_text_event(
        self,
        function: TextEventCallback,
        userdata: Any = None,
    ) -> None:
        """
        registers a callback function that gets called whenever text is entered.

        Parameters
        ----------
        function

            a callback function that receives the entered text as first
            parameter and the userdata as second parameter.

        userdata

            userdata which will be passed to the function
        """

        if self._text_event_count == 0:
            pygame.key.start_text_input()

        self._registered_events.append(TextEvent(function=function, userdata=userdata))
        self._text_event_count += 1

    def remove_text_event(self, function: TextEventCallback) -> None:
        """
        removes a callback function previously registered with
        :meth:`~pyage.event_processor.EventProcessor.add_text_event`

        Parameters
        ----------
        function

            the callback function
        """

        f: Event

        for f in self._registered_events:
            if (
                f not in self._unregistered_events
                and f.type == EVENT.TEXT
                and f.function == function
            ):
                self._unregistered_events.append(f)
                self._text_event_count -= 1

        if self._text_event_count <= 0:
            self._text_event_count = 0
            pygame.key.stop_text_input()
