import traceback
from typing import Any, Callable, List, cast

import pygame

from pyage.constants import EVENT
from pyage.event import Event
from pyage.events.focus import FocusEvent
from pyage.events.key import KeyEvent


class EventProcessor:

    _registered_events: List[Event] = []
    _unregistered_events: List[Event] = []

    def _process(self, e: Any) -> None:

        f: Event

        if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:

            events: List[KeyEvent] = []

            f_type: int = EVENT.KEYDOWN

            if e.type == pygame.KEYUP:
                f_type = EVENT.KEYUP

            for f in self._registered_events:
                if (
                    f.Type == f_type
                    and cast(KeyEvent, f).Key == e.key
                    and e.mod & cast(KeyEvent, f).Mod == cast(KeyEvent, f).Mod
                ):
                    if cast(KeyEvent, f).Mod != 0:
                        events = [cast(KeyEvent, f)] + events
                    else:
                        events.append(cast(KeyEvent, f))

            if len(events) > 0:
                events[0].Function(
                    KeyUp=(False if events[0].Type == EVENT.KEYDOWN else True)
                )

            """
        if events[0].Repeat > 0:
          EventSpawner.SpawnerListLock.acquire()
          if len(EventSpawner.SpawnerList)==0:
            EventSpawner(PossibleStack[0]['key'],PossibleStack[0]['mod'],PossibleStack[0]['repeat']).start()
          EventSpawner.SpawnerListLock.release()
      """

        elif e.type == pygame.ACTIVEEVENT:

            if e.state == 1:
                return

            for f in self._registered_events:
                if f.Type == EVENT.FOCUS:
                    f.Function(bool(e.gain))

    def Process(self) -> None:
        try:
            events = pygame.event.get()
        except pygame.error:
            return

        for e in events:
            if e.type != pygame.NOEVENT:
                try:
                    self._process(e)
                except BaseException:
                    print(
                        "exception encountered and silently ignored:\n",
                        traceback.format_exc(),
                    )

    def AddKeyDownEvent(
        self, function: Callable[[bool], None], key: int, mod: int = 0, repeat: int = 0
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
                and f.Type == EVENT.KEYDOWN
                and cast(KeyEvent, f).Key == key
                and cast(KeyEvent, f).Mod == mod
            ):
                self._unregistered_events.append(f)

    def DelKeyUpEvent(self, key: int, mod: int = 0) -> None:

        f: Event

        for f in self._registered_events:
            if (
                f not in self._unregistered_events
                and f.Type == EVENT.KEYUP
                and cast(KeyEvent, f).Key == key
                and cast(KeyEvent, f).Mod == mod
            ):
                self._unregistered_events.append(f)

    def DelFocusEvent(self, function: Callable[[bool], None]) -> None:

        f: Event

        for f in self._registered_events:
            if (
                f not in self._unregistered_events
                and f.Type == EVENT.FOCUS
                and f.Function == function
            ):
                self._unregistered_events.append(f)

    def DelAllKeyEvents(self) -> None:

        events: List[Event] = [
            f
            for f in self._registered_events
            if f not in self._unregistered_events
            and (f.Type == EVENT.KEYDOWN or f.Type == EVENT.KEYUP)
        ]

        self._unregistered_events = self._unregistered_events + events
