import copy
import heapq
import time
import traceback
from typing import Callable, List, Optional, Tuple, cast

import pygame

from pyage.constants import EVENT, KEY, MOD
from pyage.event import Event
from pyage.events.focus import FocusEvent
from pyage.events.key import KeyEvent


class EventProcessor:

    _event_queue: List[Tuple[float, Event]] = []
    _registered_events: List[Event] = []
    _unregistered_events: List[Event] = []

    def _process_pygame_event(self, e: pygame.event.EventType) -> None:

        f: Optional[Event]
        r_f: Event

        if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:

            try:
                f = next(
                    r_f
                    for r_f in self._registered_events
                    if r_f._type == EVENT.KEY
                    and cast(KeyEvent, r_f)._key == e.key
                    and e.mod & cast(KeyEvent, r_f)._mod == cast(KeyEvent, r_f)._mod
                )
            except StopIteration:
                f = None

            if f:

                r_f = copy.copy(f)
                cast(KeyEvent, r_f)._pressed = (
                    True if e.type == pygame.KEYDOWN else False
                )

                heapq.heappush(
                    self._event_queue,
                    (
                        time.time(),
                        r_f,
                    ),
                )

        elif e.type == pygame.ACTIVEEVENT:

            if e.state == 1:
                return

            for f in self._registered_events:

                if f._type == EVENT.FOCUS:

                    r_f = copy.copy(f)
                    cast(FocusEvent, r_f)._gain = bool(e.gain)

                    heapq.heappush(
                        self._event_queue,
                        (
                            time.time(),
                            r_f,
                        ),
                    )

    def _process_event(self, e: Event) -> None:

        keys: Tuple[int]

        if e in self._unregistered_events:
            return

        if e._type == EVENT.KEY:

            if cast(KeyEvent, e)._pressed and cast(KeyEvent, e)._repeat > 0:

                keys = pygame.key.get_pressed()

                if (
                    cast(KeyEvent, e)._mod == 0
                    and not bool(keys[cast(KeyEvent, e)._key])
                ) or (
                    cast(KeyEvent, e)._mod != 0
                    and (
                        pygame.key.get_mods() & cast(KeyEvent, e)._mod
                        != cast(KeyEvent, e)._mod
                        or not bool(keys[cast(KeyEvent, e)._key])
                    )
                ):
                    return

            e.Function(cast(KeyEvent, e)._pressed)

            if cast(KeyEvent, e)._repeat > 0 and cast(KeyEvent, e)._pressed:
                heapq.heappush(
                    self._event_queue,
                    (
                        time.time() + cast(KeyEvent, e)._repeat,
                        e,
                    ),
                )

        elif e._type == EVENT.FOCUS:
            e.Function(cast(FocusEvent, e)._gain)

    def _unregister_event(self, e: Event) -> None:

        try:
            self._registered_events.remove(e)
        except ValueError:
            pass

    def Process(self) -> None:

        e: pygame.event.EventType
        f: Event
        events: List[pygame.event.EventType]

        try:
            events = pygame.event.get()
        except pygame.error:
            return

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

    def AddKeyEvent(
        self,
        function: Callable[[bool], None],
        key: KEY,
        mod: MOD = MOD.NONE,
        repeat: float = 0.0,
    ) -> None:

        self._registered_events.append(
            KeyEvent(function=function, key=key, mod=mod, repeat=repeat)
        )

    def AddFocusEvent(self, function: Callable[[bool], None]) -> None:

        self._registered_events.append(FocusEvent(function))

    def DelKeyEvent(self, key: int, mod: int = 0) -> None:

        f: Event

        for f in self._registered_events:
            if (
                f not in self._unregistered_events
                and f._type == EVENT.KEY
                and cast(KeyEvent, f)._key == key
                and cast(KeyEvent, f)._mod == mod
            ):
                self._unregistered_events.append(f)

    def DelFocusEvent(self, function: Callable[[bool], None]) -> None:

        f: Event

        for f in self._registered_events:
            if (
                f not in self._unregistered_events
                and f._type == EVENT.FOCUS
                and f._function == function
            ):
                self._unregistered_events.append(f)

    def DelAllKeyEvents(self) -> None:

        events: List[Event] = [
            f
            for f in self._registered_events
            if f not in self._unregistered_events and (f._type == EVENT.KEY)
        ]

        self._unregistered_events = self._unregistered_events + events
