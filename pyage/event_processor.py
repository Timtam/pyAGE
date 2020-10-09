import copy
import heapq
import time
import traceback
from typing import Callable, List, Optional, Tuple, cast

import pygame

from pyage.constants import EVENT
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

            f_type: int = EVENT.KEYDOWN

            if e.type == pygame.KEYUP:
                f_type = EVENT.KEYUP

            try:
                f = next(
                    r_f
                    for r_f in self._registered_events
                    if r_f._type == f_type
                    and cast(KeyEvent, r_f)._key == e.key
                    and e.mod & cast(KeyEvent, r_f)._mod == cast(KeyEvent, r_f)._mod
                )
            except StopIteration:
                f = None

            if f:
                heapq.heappush(
                    self._event_queue,
                    (
                        time.time(),
                        f,
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

        if e in self._unregistered_events:
            return

        if e._type == EVENT.KEYDOWN or e._type == EVENT.KEYUP:
            e.Function(True if e._type == EVENT.KEYUP else False)
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

        try:
            while f := self._unregistered_events.pop():
                self._unregister_event(f)
        except IndexError:
            pass

    def AddKeyDownEvent(
        self,
        function: Callable[[bool], None],
        key: int,
        mod: int = 0,
        repeat: float = 0.0,
    ) -> None:

        self._registered_events.append(
            KeyEvent(
                type=EVENT.KEYDOWN, function=function, key=key, mod=mod, repeat=repeat
            )
        )

    def AddKeyUpEvent(
        self, function: Callable[[bool], None], key: int, mod: int = 0
    ) -> None:

        self._registered_events.append(
            KeyEvent(type=EVENT.KEYUP, key=key, mod=mod, function=function)
        )

    def AddFocusEvent(self, function: Callable[[bool], None]) -> None:

        self._registered_events.append(FocusEvent(function))

    def DelKeyDownEvent(self, key: int, mod: int = 0) -> None:

        f: Event

        for f in self._registered_events:
            if (
                f not in self._unregistered_events
                and f._type == EVENT.KEYDOWN
                and cast(KeyEvent, f)._key == key
                and cast(KeyEvent, f)._mod == mod
            ):
                self._unregistered_events.append(f)

    def DelKeyUpEvent(self, key: int, mod: int = 0) -> None:

        f: Event

        for f in self._registered_events:
            if (
                f not in self._unregistered_events
                and f._type == EVENT.KEYUP
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
            if f not in self._unregistered_events
            and (f._type == EVENT.KEYDOWN or f._type == EVENT.KEYUP)
        ]

        self._unregistered_events = self._unregistered_events + events
